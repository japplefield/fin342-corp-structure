#!/usr/bin/env python3
import sys
sys.path.insert(1, 'handle_data/')
import model
import statistics
import matplotlib.pyplot as plt
import numpy
from matplotlib import rcParams
from labellines import labelLine, labelLines

rcParams['figure.figsize'] = [12, 7]

con = model.sql_connection()
cur = con.cursor()

# Get GICS Unique sectors
cur.execute("SELECT DISTINCT sector FROM gics")
rows = cur.fetchall()
unique_sectors = [dct['sector'] for dct in rows]

quarters = ['Q32019'] + list(model.quarters)
#Print Debt Change Line Graph by GICS sector
NUM_COLORS = len(unique_sectors) + 1
cm = plt.get_cmap('gist_rainbow')

i = 0
# Calcuate Summary Median Debt Cng/EBITDA for each Sector
meds = {}
for sector in unique_sectors:
    cur.execute("SELECT     debt_cng_ebd.Q42019 + eq_cng_tot_ebd_2.Q42019 AS Q42019, "
                "debt_cng_ebd.Q12020 + eq_cng_tot_ebd_2.Q12020 AS Q12020, "
                "debt_cng_ebd.Q22020 + eq_cng_tot_ebd_2.Q22020 AS Q22020, "
                "debt_cng_ebd.Q32020 + eq_cng_tot_ebd_2.Q32020 AS Q32020 "
                "FROM       debt_cng_ebd "
                "INNER JOIN eq_cng_tot_ebd_2 "
                "INNER JOIN gics "
                "ON         debt_cng_ebd.symbol=gics.symbol "
                "AND        debt_cng_ebd.symbol=eq_cng_tot_ebd_2.symbol "
                "where      gics.sector=?", [sector])
    rows = cur.fetchall()
    meds[sector] = {quarter: statistics.median([row[quarter] for row in rows]) for quarter in model.quarters}
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    plt.xticks(numpy.arange(5), quarters)
    plt.ylim(-0.3, 0.5)
    plt.plot(range(5), [0] + [sum(list(meds[sector].values())[:(i+1)]) for i in range(len(model.quarters))],  label=sector, color=cm(1.*i/NUM_COLORS))
    i += 1
    plt.xlabel('Quarter')
    ax.axhline(color='black')
    plt.ylabel('Median Cumulative Debt + Equity Change/Normalized EBITDA')
    plt.title(f'Median Cumulative Debt + Equity Change/Normalized EBITDA for {sector}')
    plt.tight_layout()
    plt.savefig(f'Total Cumulative Line Charts/med_tot_eq_debt_cng_ebitda_cum_{sector}.png')

cur.execute("SELECT     debt_cng_ebd.Q42019 + eq_cng_tot_ebd_2.Q42019 AS Q42019, "
            "debt_cng_ebd.Q12020 + eq_cng_tot_ebd_2.Q12020 AS Q12020, "
            "debt_cng_ebd.Q22020 + eq_cng_tot_ebd_2.Q22020 AS Q22020, "
            "debt_cng_ebd.Q32020 + eq_cng_tot_ebd_2.Q32020 AS Q32020 "
            "FROM       debt_cng_ebd "
            "INNER JOIN eq_cng_tot_ebd_2 "
            "ON        debt_cng_ebd.symbol=eq_cng_tot_ebd_2.symbol")
rows = cur.fetchall()
meds['All'] = {quarter: statistics.median([row[quarter] for row in rows if row[quarter] is not None]) for quarter in model.quarters}
# Close Database
con.commit()


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(5), quarters)
plt.ylim(-0.3, 0.5)
for sector in meds:
    plt.plot(range(5), [0] + [sum(list(meds[sector].values())[:(i+1)]) for i in range(len(model.quarters))],  label=sector)
plt.xlabel('Quarter')
ax.axhline(color='black')
plt.ylabel('Median Cumulative Debt + Equity Change/Normalized EBITDA')
plt.title('Median Cumulative Debt + Equity Change/Normalized EBITDA by Sector')
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('Total Cumulative Line Charts/med_tot_eq_debt_cng_ebitda_cum_all.png')
