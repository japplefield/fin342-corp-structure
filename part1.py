import statistics
import model, file_import
import matplotlib.pyplot as plt
import numpy
from matplotlib import rcParams
from labellines import labelLine, labelLines

rcParams['figure.figsize'] = [10, 5]

con = model.sql_connection()
cur = con.cursor()

file_import.read_files(cur)

# Get GICS Unique sectors, industry groups, industries, and sub industries for later
cur.execute("SELECT DISTINCT sector FROM gics")
rows = cur.fetchall()
unique_sectors = [dct['sector'] for dct in rows]

cur.execute("SELECT DISTINCT industry_group FROM gics")
rows = cur.fetchall()
unique_industry_groups = [dct['industry_group'] for dct in rows]

cur.execute("SELECT DISTINCT industry FROM gics")
rows = cur.fetchall()
unique_industries = [dct['industry'] for dct in rows]

cur.execute("SELECT DISTINCT sub_industry FROM gics")
rows = cur.fetchall()
unique_sub_industries = [dct['sub_industry'] for dct in rows]

# Calcuate Summary Median Debt Cng/EBITDA for each Sector
quarters = ('Q42019', 'Q12020', 'Q22020', 'Q32020')
cur.execute("SELECT * FROM debt_cng_ebd INNER JOIN gics ON debt_cng_ebd.symbol=gics.symbol")
rows = cur.fetchall()
med_sector_dbt_ebd_cng = {sector: {quarter: statistics.median([row[quarter] for row in rows]) for quarter in quarters} for sector in unique_sectors}


con.commit()
exit()

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
