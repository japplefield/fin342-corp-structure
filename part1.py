import statistics
import model, file_import
import matplotlib.pyplot as plt
import numpy
from matplotlib import rcParams
from labellines import labelLine, labelLines

rcParams['figure.figsize'] = [15, 10]

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
med_sector_dbt_ebd_cng = {}
for sector in unique_sectors:
    cur.execute("SELECT * FROM debt_cng_ebd INNER JOIN gics ON debt_cng_ebd.symbol=gics.symbol WHERE gics.sector=?", [sector])
    rows = cur.fetchall()
    med_sector_dbt_ebd_cng[sector] = {quarter: statistics.median([row[quarter] for row in rows]) for quarter in quarters}

# Calculate Summary Median Eq Cng / EBITDA for each sector
med_sector_eq_ebd_cng = {}
for sector in unique_sectors:
    cur.execute("SELECT * FROM eq_cng_ebd_2 INNER JOIN gics ON eq_cng_ebd_2.symbol=gics.symbol WHERE gics.sector=?", [sector])
    rows = cur.fetchall()
    med_sector_eq_ebd_cng[sector] = {quarter: statistics.median([row[quarter] for row in rows if row[quarter] is not None]) for quarter in quarters}

# Draw up For Airlines
cur.execute("SELECT * FROM eq_cng_ebd_2 INNER JOIN gics ON eq_cng_ebd_2.symbol=gics.symbol WHERE gics.industry='Airlines'")
airlines_eq_ebd_cng = cur.fetchall()
cur.execute("SELECT * FROM debt_cng_ebd INNER JOIN gics ON debt_cng_ebd.symbol=gics.symbol WHERE gics.industry='Airlines'")
airlines_debt_ebd_cng = cur.fetchall()

# Close Database
con.commit()

#Print Debt Change Line Graph by GICS sector
NUM_COLORS = len(unique_sectors)
cm = plt.get_cmap('gist_rainbow')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(4), quarters)
plt.ylim(-0.15, 0.5)
for sector in unique_sectors:
    plt.plot(range(4), [med_sector_dbt_ebd_cng[sector][quarter] for quarter in quarters],  label=sector)
plt.xlabel('Quarter')
plt.ylabel('Median Debt Change/Normalized EBITDA')
plt.title('Median Debt Change/Normalized EBITDA by Sector')
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('med_debt_cng_ebitda_new.png')

#Print Equity Change Line Graph by GICS sector
NUM_COLORS = len(unique_sectors)
cm = plt.get_cmap('gist_rainbow')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(4), quarters)
plt.ylim(-0.1, 0.02)
for sector in unique_sectors:
    plt.plot(range(4), [med_sector_eq_ebd_cng[sector][quarter] for quarter in quarters],  label=sector)
plt.xlabel('Quarter')
plt.ylabel('Median Equity Change/Normalized EBITDA')
plt.title('Median Equity Change/Normalized EBITDA by Sector')
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('med_eq_cng_ebitda_new.png')

exit()

#Print Equity Change Line Graph by GICS Sector





# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)


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
