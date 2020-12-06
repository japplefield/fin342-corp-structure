#!/usr/bin/env python
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

quarters = ['Q32019'] + list(model.quarters)
#Print Debt Change Line Graph by GICS sector
NUM_COLORS = len(unique_sectors)
cm = plt.get_cmap('gist_rainbow')

i = 0
# Calcuate Summary Median Debt Cng/EBITDA for each Sector
med_sector_dbt_ebd_cng = {}
for sector in unique_sectors:
    cur.execute("SELECT * FROM debt_cng_ebd INNER JOIN gics ON debt_cng_ebd.symbol=gics.symbol WHERE gics.sector=?", [sector])
    rows = cur.fetchall()
    med_sector_dbt_ebd_cng[sector] = {quarter: statistics.median([row[quarter] for row in rows]) for quarter in model.quarters}
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    plt.xticks(numpy.arange(5), quarters)
    plt.ylim(-0.15, 0.5)
    plt.plot(range(5), [0] + [sum(list(med_sector_dbt_ebd_cng[sector].values())[:(i+1)]) for i in range(len(model.quarters))],  label=sector, color=cm(1.*i/NUM_COLORS))
    i += 1
    plt.xlabel('Quarter')
    plt.ylabel('Median Cumulative Debt Change/Normalized EBITDA')
    plt.title(f'Median Cumulative Debt Change/Normalized EBITDA for {sector}')
    plt.tight_layout()
    plt.savefig(f'Debt Cumulative Line Charts/med_debt_cng_ebitda_cum_{sector}.png')

# Close Database
con.commit()


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(5), quarters)
plt.ylim(-0.15, 0.5)
for sector in unique_sectors:
    plt.plot(range(5), [0] + [sum(list(med_sector_dbt_ebd_cng[sector].values())[:(i+1)]) for i in range(len(model.quarters))],  label=sector)
plt.xlabel('Quarter')
plt.ylabel('Median Cumulative Debt Change/Normalized EBITDA')
plt.title('Median Cumulative Debt Change/Normalized EBITDA by Sector')
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('Debt Cumulative Line Charts/med_debt_cng_ebitda_cum_all.png')
