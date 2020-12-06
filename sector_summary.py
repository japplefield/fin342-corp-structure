import model
import statistics
import matplotlib.pyplot as plt
import numpy
from matplotlib import rcParams
from labellines import labelLine, labelLines

rcParams['figure.figsize'] = [15, 10]

con = model.sql_connection()
cur = con.cursor()

# Get GICS Unique sectors
cur.execute("SELECT DISTINCT sector FROM gics")
rows = cur.fetchall()
unique_sectors = [dct['sector'] for dct in rows]

# Calcuate Summary Median Debt Cng/EBITDA for each Sector
med_sector_dbt_ebd_cng = {}
for sector in unique_sectors:
    cur.execute("SELECT * FROM debt_cng_ebd INNER JOIN gics ON debt_cng_ebd.symbol=gics.symbol WHERE gics.sector=?", [sector])
    rows = cur.fetchall()
    med_sector_dbt_ebd_cng[sector] = {quarter: statistics.median([row[quarter] for row in rows]) for quarter in model.quarters}

# Calculate Summary Median 


# Calculate Summary Median Eq Cng / EBITDA for each sector
med_sector_eq_ebd_cng = {}
for sector in unique_sectors:
    cur.execute("SELECT * FROM eq_cng_ebd_2 INNER JOIN gics ON eq_cng_ebd_2.symbol=gics.symbol WHERE gics.sector=?", [sector])
    rows = cur.fetchall()
    med_sector_eq_ebd_cng[sector] = {quarter: statistics.median([row[quarter] for row in rows if row[quarter] is not None]) for quarter in model.quarters}

# Close Database
con.commit()

#Print Debt Change Line Graph by GICS sector
NUM_COLORS = len(unique_sectors)
cm = plt.get_cmap('gist_rainbow')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(4), model.quarters)
plt.ylim(-0.15, 0.5)
for sector in unique_sectors:
    plt.plot(range(4), [med_sector_dbt_ebd_cng[sector][quarter] for quarter in model.quarters],  label=sector)
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
plt.xticks(numpy.arange(4), model.quarters)
plt.ylim(-0.1, 0.02)
for sector in unique_sectors:
    plt.plot(range(4), [med_sector_eq_ebd_cng[sector][quarter] for quarter in model.quarters],  label=sector)
plt.xlabel('Quarter')
plt.ylabel('Median Equity Change/Normalized EBITDA')
plt.title('Median Equity Change/Normalized EBITDA by Sector')
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('med_eq_cng_ebitda_new.png')
