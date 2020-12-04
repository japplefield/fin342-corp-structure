#!/usr/bin/env python3
import csv
import statistics
import matplotlib.pyplot as plt
import numpy
from matplotlib import rcParams
from labellines import labelLine, labelLines
from datetime import datetime, timedelta
import sqlite3
rcParams['figure.figsize'] = [10, 5]

def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.
    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def sql_connection():
    try:
        con = sqlite3.connect('project.db')
        con.row_factory = dict_factory
        return con
    except sqlite3.Error:
        print(sqlite3.Error)

cur = sql_connection().cursor()

data_dict = {}
summary = {}
unique_sectors = set()
unique_industry_groups = set()
unique_industries = set()
unique_sub_industries = set()

# Read in each company's ticker, Sector, and Industry Group
with open('SP1500GICS.csv', newline='', encoding='utf-8-sig') as ifh:
    reader = csv.DictReader(ifh)
    for row in reader:
        data_dict[row['Symbol']] = {}
        data_dict[row['Symbol']]['Sector'] = row['GICS Sector']
        if row['GICS Sector'] not in unique_sectors and row['GICS Sector'] != '#N/A':
            unique_sectors.add(row['GICS Sector'])
        data_dict[row['Symbol']]['Industry Group'] = row['GICS Industry Group']
        if row['GICS Industry Group'] not in unique_industry_groups and row['GICS Industry Group'] != '#N/A':
            unique_industry_groups.add(row['GICS Industry Group'])
        data_dict[row['Symbol']]['Industry'] = row['GICS Industry']
        if row['GICS Industry'] not in unique_industries and row['GICS Industry'] != '#N/A':
            unique_industries.add(row['GICS Industry'])
        data_dict[row['Symbol']]['Sub-Industry'] = row['GICS Sub-Industry']
        if row['GICS Sub-Industry'] not in unique_sub_industries and row['GICS Sub-Industry'] != '#N/A':
            unique_sub_industries.add(row['GICS Sub-Industry'])

# Calculate Normalized EBITDA for each company
with open('SP1500EBITDA.csv', newline='') as ifh:
    ifh.readline()
    for row in ifh:
        data = row.strip().split(',')
        ticker = data[0]
        data = data[1:]
        try:
            data_dict[ticker]['EBITDA'] = statistics.mean([float(ebitda) for ebitda in data])
        except ValueError:
            data_dict.pop(ticker)

# Calculate Debt / Normialized EBITDA for each company for each of the 5 quarters and Cng Debt / Normalized EBITDA for the 4 periods
with open('SP1500Debt.csv', newline='', encoding='utf-8-sig') as ifH:
    reader = csv.DictReader(ifH)
    for row in reader:
        try:
            ticker = row['Symbol']
            data_dict[ticker]['Q3 2019 Debt/EBITDA'] = float(row['Q3 2019 Debt']) / data_dict[ticker]['EBITDA']
            data_dict[ticker]['Q4 2019 Debt/EBITDA'] = float(row['Q4 2019 Debt']) / data_dict[ticker]['EBITDA']
            data_dict[ticker]['Q4 2019 Debt Cng/EBITDA'] = (float(row['Q4 2019 Debt']) - float(row['Q3 2019 Debt'])) / data_dict[ticker]['EBITDA']
            data_dict[ticker]['Q1 2020 Debt/EBITDA'] = float(row['Q1 2020 Debt']) / data_dict[ticker]['EBITDA']
            data_dict[ticker]['Q1 2020 Debt Cng/EBITDA'] = (float(row['Q1 2020 Debt']) - float(row['Q4 2019 Debt'])) / data_dict[ticker]['EBITDA']
            data_dict[ticker]['Q2 2020 Debt/EBITDA'] = float(row['Q2 2020 Debt']) / data_dict[ticker]['EBITDA']
            data_dict[ticker]['Q2 2020 Debt Cng/EBITDA'] = (float(row['Q2 2020 Debt']) - float(row['Q1 2020 Debt'])) / data_dict[ticker]['EBITDA']
            data_dict[ticker]['Q3 2020 Debt/EBITDA'] = float(row['Q3 2020 Debt']) / data_dict[ticker]['EBITDA']
            data_dict[ticker]['Q3 2020 Debt Cng/EBITDA'] = (float(row['Q3 2020 Debt']) - float(row['Q2 2020 Debt'])) / data_dict[ticker]['EBITDA']
        except KeyError:
            pass
        except ValueError:
            pass

# Calcuate Summary Median Debt/EBITDA for each Sector
med_debt_ebitda = {}
for sector in unique_sectors:
    med_debt_ebitda[sector] = {}
    med_debt_ebitda[sector]['Q3 2019'] = statistics.median([data_dict[ticker]['Q3 2019 Debt/EBITDA'] for ticker in data_dict if data_dict[ticker]['Sector'] == sector and 'Q3 2019 Debt/EBITDA' in data_dict[ticker]])
    med_debt_ebitda[sector]['Q4 2019'] = statistics.median([data_dict[ticker]['Q4 2019 Debt/EBITDA'] for ticker in data_dict if data_dict[ticker]['Sector'] == sector and 'Q4 2019 Debt/EBITDA' in data_dict[ticker]])
    med_debt_ebitda[sector]['Q1 2020'] = statistics.median([data_dict[ticker]['Q1 2020 Debt/EBITDA'] for ticker in data_dict if data_dict[ticker]['Sector'] == sector and 'Q1 2020 Debt/EBITDA' in data_dict[ticker]])
    med_debt_ebitda[sector]['Q2 2020'] = statistics.median([data_dict[ticker]['Q2 2020 Debt/EBITDA'] for ticker in data_dict if data_dict[ticker]['Sector'] == sector and 'Q2 2020 Debt/EBITDA' in data_dict[ticker]])
    med_debt_ebitda[sector]['Q3 2020'] = statistics.median([data_dict[ticker]['Q3 2020 Debt/EBITDA'] for ticker in data_dict if data_dict[ticker]['Sector'] == sector and 'Q3 2020 Debt/EBITDA' in data_dict[ticker]])

#Print Debt Change Line Graph by GICS Sector
quarters = ('Q3 2019','Q4 2019', 'Q1 2020', 'Q2 2020', 'Q3 2020')
NUM_COLORS = len(unique_sectors)
cm = plt.get_cmap('gist_rainbow')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(5), quarters)
plt.ylim(1.5, 4.5)
for sector in unique_sectors:
    plt.plot(range(5), [med_debt_ebitda[sector][quarter] for quarter in quarters],  label=sector)
plt.xlabel('Quarter')
plt.ylabel('Median Debt/Normalized EBITDA')
plt.title('Median Debt/Normalized EBITDA by Sector')
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('med_debt_ebitda.png')


# Calcuate Summary Median Debt Cng/EBITDA for each Sector
med_debt_ebitda_cng = {}
for sector in unique_sectors:
    med_debt_ebitda_cng[sector] = {}
    med_debt_ebitda_cng[sector]['Q4 2019'] = statistics.median([data_dict[ticker]['Q4 2019 Debt Cng/EBITDA'] for ticker in data_dict if data_dict[ticker]['Sector'] == sector and 'Q4 2019 Debt Cng/EBITDA' in data_dict[ticker]])
    med_debt_ebitda_cng[sector]['Q1 2020'] = statistics.median([data_dict[ticker]['Q1 2020 Debt Cng/EBITDA'] for ticker in data_dict if data_dict[ticker]['Sector'] == sector and 'Q1 2020 Debt Cng/EBITDA' in data_dict[ticker]])
    med_debt_ebitda_cng[sector]['Q2 2020'] = statistics.median([data_dict[ticker]['Q2 2020 Debt Cng/EBITDA'] for ticker in data_dict if data_dict[ticker]['Sector'] == sector and 'Q2 2020 Debt Cng/EBITDA' in data_dict[ticker]])
    med_debt_ebitda_cng[sector]['Q3 2020'] = statistics.median([data_dict[ticker]['Q3 2020 Debt Cng/EBITDA'] for ticker in data_dict if data_dict[ticker]['Sector'] == sector and 'Q3 2020 Debt Cng/EBITDA' in data_dict[ticker]])

#Print Debt Change Line Graph by GICS Sector
quarters = ('Q4 2019', 'Q1 2020', 'Q2 2020', 'Q3 2020')
NUM_COLORS = len(unique_sectors)
cm = plt.get_cmap('gist_rainbow')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(4), quarters)
plt.ylim(-0.25, 0.5)
for sector in unique_sectors:
    plt.plot(range(4), [med_debt_ebitda_cng[sector][quarter] for quarter in quarters],  label=sector)
plt.xlabel('Quarter')
plt.ylabel('Median Debt Change/Normalized EBITDA')
plt.title('Median Debt Change/Normalized EBITDA by Sector')
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('med_debt_cng_ebitda.png')

#Calculate Average price for each quarter for each firm
Q419ST = datetime.strptime("10/01/2019", "%m/%d/%Y")
Q120ST = datetime.strptime("01/01/2020", "%m/%d/%Y")
Q220ST = datetime.strptime("04/01/2020", "%m/%d/%Y")
Q320ST = datetime.strptime("07/01/2020", "%m/%d/%Y")
Q420ST = datetime.strptime("10/01/2020", "%m/%d/%Y")

with open('SP1500DatedPrices.csv', newline='', encoding='utf-8-sig') as ifh:
    reader = csv.DictReader(ifh)
    for row in reader:
        ticker = row['Symbol']
        if ticker in data_dict:
            data_dict[ticker]['Q319AvgP'] = statistics.mean([ float(row[date]) for date in reader.fieldnames[1:]  if datetime.strptime(date, "%m/%d/%Y") < Q419ST ])
            data_dict[ticker]['Q419AvgP'] = statistics.mean([ float(row[date]) for date in reader.fieldnames[1:]  if datetime.strptime(date, "%m/%d/%Y") < Q120ST ])
            data_dict[ticker]['Q120AvgP'] = statistics.mean([ float(row[date]) for date in reader.fieldnames[1:]  if datetime.strptime(date, "%m/%d/%Y") < Q220ST ])
            data_dict[ticker]['Q220AvgP'] = statistics.mean([ float(row[date]) for date in reader.fieldnames[1:]  if datetime.strptime(date, "%m/%d/%Y") < Q320ST ])
            data_dict[ticker]['Q320AvgP'] = statistics.mean([ float(row[date]) for date in reader.fieldnames[1:]  if datetime.strptime(date, "%m/%d/%Y") < Q420ST ])

#Calculate change in equity value from share issuance (buybacks)
with open('SP1500SharesOutstanding.csv', newline='', encoding='utf-8-sig') as ifh:
    reader = csv.DictReader(ifh)
    for row in reader:
        ticker = row['Symbol']
        if ticker in data_dict:
            try:
                data_dict[ticker]['Q419EqCng'] = (float(row['Q4 2019 Shares Outstanding']) - float(row['Q3 2019 Shares Outstanding'])) * data_dict[ticker]['Q419AvgP']
                data_dict[ticker]['Q419EndShares'] = float(row['Q4 2019 Shares Outstanding'])
            except ValueError:
                pass
            try:
                data_dict[ticker]['Q120EqCng'] = (float(row['Q1 2020 Shares Outstanding']) - float(row['Q4 2019 Shares Outstanding'])) * data_dict[ticker]['Q120AvgP']
                data_dict[ticker]['Q120EndShares'] = float(row['Q1 2020 Shares Outstanding'])
            except ValueError:
                pass
            try:
                data_dict[ticker]['Q220EqCng'] = (float(row['Q2 2020 Shares Outstanding']) - float(row['Q1 2020 Shares Outstanding'])) * data_dict[ticker]['Q220AvgP']
                data_dict[ticker]['Q220EndShares'] = float(row['Q2 2020 Shares Outstanding'])
            except ValueError:
                pass
            try:
                data_dict[ticker]['Q320EqCng'] = (float(row['Q3 2020 Shares Outstanding']) - float(row['Q2 2020 Shares Outstanding'])) * data_dict[ticker]['Q320AvgP']
                data_dict[ticker]['Q320EndShares'] = float(row['Q3 2020 Shares Outstanding'])
            except ValueError:
                pass

#Adjust for Dividends
with open('SP1500DividendsPerShare.csv', newline='', encoding='utf-8-sig') as ifh:
    reader = csv.DictReader(ifh)
    for row in reader:
        ticker = row['Symbol']
        #﻿Symbol,Q3 2019 Dividend per Share,Q4 2019 Dividend per Share,Q1 2020 Dividend per Share,Q2 2020 Dividend per Share,Q3 2020 Dividend per Share
        if ticker in data_dict:
            try:
                if row['Q4 2019 Dividend per Share'] != '#N/A':
                    data_dict[ticker]['Q419EqCng'] -= float(row['Q4 2019 Dividend per Share']) * data_dict[ticker]['Q419EndShares']
                data_dict[ticker]['Q4 2019 Eq Cng/EBITDA'] = data_dict[ticker]['Q419EqCng'] / data_dict[ticker]['EBITDA']
                if row['Q1 2020 Dividend per Share'] != '#N/A':
                    data_dict[ticker]['Q120EqCng'] -= float(row['Q1 2020 Dividend per Share']) * data_dict[ticker]['Q120EndShares']
                data_dict[ticker]['Q1 2020 Eq Cng/EBITDA'] = data_dict[ticker]['Q120EqCng'] / data_dict[ticker]['EBITDA']
                if row['Q2 2020 Dividend per Share'] != '#N/A':
                    data_dict[ticker]['Q220EqCng'] -= float(row['Q2 2020 Dividend per Share']) * data_dict[ticker]['Q220EndShares']
                data_dict[ticker]['Q2 2020 Eq Cng/EBITDA'] = data_dict[ticker]['Q220EqCng'] / data_dict[ticker]['EBITDA']
                if row['Q3 2020 Dividend per Share'] != '#N/A':
                    data_dict[ticker]['Q320EqCng'] -= float(row['Q3 2020 Dividend per Share']) * data_dict[ticker]['Q320EndShares']
                data_dict[ticker]['Q3 2020 Eq Cng/EBITDA'] = data_dict[ticker]['Q320EqCng'] / data_dict[ticker]['EBITDA']
            except KeyError:
                pass
            except ValueError:
                pass

# Calcuate Summary Median Equity Cng/EBITDA for each Sector
med_eq_ebitda_cng = {}
for sector in unique_sectors:
    med_eq_ebitda_cng[sector] = {}
    med_eq_ebitda_cng[sector]['Q4 2019'] = statistics.median([data_dict[ticker]['Q4 2019 Eq Cng/EBITDA'] for ticker in data_dict if data_dict[ticker]['Sector'] == sector and 'Q4 2019 Eq Cng/EBITDA' in data_dict[ticker]])
    med_eq_ebitda_cng[sector]['Q1 2020'] = statistics.median([data_dict[ticker]['Q1 2020 Eq Cng/EBITDA'] for ticker in data_dict if data_dict[ticker]['Sector'] == sector and 'Q1 2020 Eq Cng/EBITDA' in data_dict[ticker]])
    med_eq_ebitda_cng[sector]['Q2 2020'] = statistics.median([data_dict[ticker]['Q2 2020 Eq Cng/EBITDA'] for ticker in data_dict if data_dict[ticker]['Sector'] == sector and 'Q2 2020 Eq Cng/EBITDA' in data_dict[ticker]])
    med_eq_ebitda_cng[sector]['Q3 2020'] = statistics.median([data_dict[ticker]['Q3 2020 Eq Cng/EBITDA'] for ticker in data_dict if data_dict[ticker]['Sector'] == sector and 'Q3 2020 Eq Cng/EBITDA' in data_dict[ticker]])

#Print Equity Change Line Graph by GICS Sector
NUM_COLORS = len(unique_sectors)
cm = plt.get_cmap('gist_rainbow')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(4), quarters)
plt.ylim(-0.15, 0.02)
for sector in unique_sectors:
    plt.plot(range(4), [med_eq_ebitda_cng[sector][quarter] for quarter in quarters],  label=sector)
plt.xlabel('Quarter')
plt.ylabel('Median Equity Change/Normalized EBITDA')
plt.title('Median Equity Change/Normalized EBITDA by Sector')
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('med_eq_cng_ebitda.png')

# Print Debt Change Line Graph for Airlines
airline_debt_cng_sum = { ticker: {} for ticker in data_dict if data_dict[ticker]['Industry'] == 'Airlines' }
for airline in airline_debt_cng_sum:
    airline_debt_cng_sum[airline] = {quarters[0]: data_dict[airline]['Q4 2019 Debt Cng/EBITDA'],
                                     quarters[1]: data_dict[airline]['Q1 2020 Debt Cng/EBITDA'],
                                     quarters[2]: data_dict[airline]['Q2 2020 Debt Cng/EBITDA'],
                                     quarters[3]: data_dict[airline]['Q3 2020 Debt Cng/EBITDA']}

NUM_COLORS = len(airline_debt_cng_sum)
cm = plt.get_cmap('gist_rainbow')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(4), quarters)
plt.ylim(-0.3, 1.5)
for airline in airline_debt_cng_sum:
    plt.plot(range(4), [airline_debt_cng_sum[airline][quarter] for quarter in quarters],  label=airline)
plt.xlabel('Quarter')
plt.ylabel('Debt Change/Normalized EBITDA')
plt.title('Debt Change/Normalized EBITDA (Airlines)')
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('airline_debt_cng_ebitda.png')

# Print Equity Change Line Graph for Airlines
airline_eq_cng_sum = { ticker: {} for ticker in data_dict if data_dict[ticker]['Industry'] == 'Airlines' }
for airline in airline_eq_cng_sum:
    airline_eq_cng_sum[airline] = {quarters[0]: data_dict[airline]['Q4 2019 Eq Cng/EBITDA'],
                                   quarters[1]: data_dict[airline]['Q1 2020 Eq Cng/EBITDA'],
                                   quarters[2]: data_dict[airline]['Q2 2020 Eq Cng/EBITDA'],
                                   quarters[3]: data_dict[airline]['Q3 2020 Eq Cng/EBITDA']}

NUM_COLORS = len(airline_eq_cng_sum)
cm = plt.get_cmap('gist_rainbow')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(4), quarters)
plt.ylim(-0.3, 0.9)
for airline in airline_eq_cng_sum:
    plt.plot(range(4), [airline_eq_cng_sum[airline][quarter] for quarter in quarters],  label=airline)
plt.xlabel('Quarter')
plt.ylabel('Equity Change/Normalized EBITDA')
plt.title('Equity Change/Normalized EBITDA (Airlines)')
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('airline_eq_cng_ebitda.png')
