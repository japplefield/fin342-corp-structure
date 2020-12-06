import model
import statistics
import matplotlib.pyplot as plt
import numpy
from matplotlib import rcParams
from labellines import labelLine, labelLines

rcParams['figure.figsize'] = [25, 10]

con = model.sql_connection()
cur = con.cursor()

# Get GICS Unique sectors
cur.execute("SELECT DISTINCT sector FROM gics")
rows = cur.fetchall()
unique_sectors = [dct['sector'] for dct in rows]


meds = {}
# Calculate Summary Median Eq Cng / EBITDA for each sector
for sector in unique_sectors:
    cur.execute("SELECT * FROM eq_cng_tot_ebd_2 INNER JOIN gics ON eq_cng_tot_ebd_2.symbol=gics.symbol WHERE gics.sector=?", [sector])
    rows = cur.fetchall()
    meds[sector] = {quarter: statistics.median([row[quarter] for row in rows if row[quarter] is not None]) for quarter in model.quarters}

# Close Database
con.commit()

x = numpy.arange(len(unique_sectors))
width = 0.2
fig, ax = plt.subplots()
q4 = ax.bar(x - 1.5*width, [meds[sector][model.quarters[0]] for sector in meds], width, label=model.quarters[0])
q1 = ax.bar(x - 0.5*width, [meds[sector][model.quarters[1]] for sector in meds], width, label=model.quarters[1])
q2 = ax.bar(x + 0.5*width, [meds[sector][model.quarters[2]] for sector in meds], width, label=model.quarters[2])
q3 = ax.bar(x + 1.5*width, [meds[sector][model.quarters[3]] for sector in meds], width, label=model.quarters[3])

ax.set_ylabel('Median Equity Change / EBITDA')
ax.set_title('Median Equity Change / EBITDA by Sector, Last 4 Quarters')
ax.set_xticks(x)
ax.set_xticklabels(unique_sectors)
ax.legend()
plt.savefig('sum.png')
