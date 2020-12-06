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

#Print Shares Equity Change Line Graph by GICS sector
NUM_COLORS = len(unique_sectors)
cm = plt.get_cmap('gist_rainbow')

i = 0
med_sector_eq_cng_shares_ebd = {}
for sector in unique_sectors:
    cur.execute("SELECT * FROM eq_cng_shares_ebd_2 INNER JOIN gics ON eq_cng_shares_ebd_2.symbol=gics.symbol WHERE gics.sector=?", [sector])
    rows = cur.fetchall()
    med_sector_eq_cng_shares_ebd[sector] = {quarter: statistics.median([row[quarter] for row in rows if row[quarter] is not None]) for quarter in model.quarters}
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    plt.xticks(numpy.arange(5), quarters)
    plt.ylim(-0.01, 0.05)
    plt.plot(range(5), [0] + [sum(list(med_sector_eq_cng_shares_ebd[sector].values())[:(i+1)]) for i in range(len(model.quarters))],  label=sector, color=cm(1.*i/NUM_COLORS))
    i += 1
    plt.xlabel('Quarter')
    plt.ylabel('Median Cumulative Equity Change from Share Issuance (Repurchase) /Normalized EBITDA')
    plt.title(f'Median Cumulative Equity Change from Share Issuance (Repurchase) /Normalized EBITDA for {sector}')
    plt.tight_layout()
    plt.savefig(f'Equity Cumulative Line Charts/med_eq_shares_cng_ebitda_cum_{sector}.png')

# Close Database
con.commit()


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(5), quarters)
plt.ylim(-0.01, 0.05)
for sector in unique_sectors:
    plt.plot(range(5), [0] + [sum(list(med_sector_eq_cng_shares_ebd[sector].values())[:(i+1)]) for i in range(len(model.quarters))],  label=sector)
plt.xlabel('Quarter')
plt.ylabel('Median Cumulative Equity Change from Share Issuance (Repurchase) /Normalized EBITDA')
plt.title('Median Cumulative Equity Change from Share Issuance (Repurchase) /Normalized EBITDA by Sector')
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('Equity Cumulative Line Charts/med_eq_shares_cng_ebitda_cum_all.png')
