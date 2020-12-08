#!/usr/bin/env python
import sys
sys.path.insert(1, 'handle_data/')
import model
import statistics
import matplotlib.pyplot as plt
import numpy
from matplotlib import rcParams
from labellines import labelLine, labelLines

rcParams['figure.figsize'] = [10, 10]

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
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.bar(numpy.arange(len(meds[sector].values())), meds[sector].values(), align='center')
    plt.ylabel('Median Equity Change / Normalized EBITDA')
    ax.text(0.5, -0.05, f'Median Quarterly Equity Change / Normalized EBITDA for {sector}', ha="center", va="top", transform=ax.transAxes)
    plt.xticks(numpy.arange(len(meds[sector].values())), model.quarters)
    plt.ylim(-0.1, 0.015)
    ax = plt.gca()
    ax.set_xticklabels([])
    ax.spines["bottom"].set_position(("data", 0))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    label_offset = 0.005
    for quarter, (x_position, y_position) in zip(model.quarters, enumerate(meds[sector].values())):
        if y_position > 0:
            label_y = -label_offset
        else:
            label_y = y_position - label_offset
        ax.text(x_position, label_y, quarter, ha="center", va="top")
    plt.savefig(f'Equity Bar Charts/med_eq_tot_cng_ebitda_{sector}.png')


# Close Database
con.commit()

rcParams['figure.figsize'] = [12, 7]
x = numpy.arange(len(unique_sectors))
width = 0.2
fig, ax = plt.subplots()
q4 = ax.bar(x - 1.5*width, [meds[sector][model.quarters[0]] for sector in meds], width, label=model.quarters[0])
q1 = ax.bar(x - 0.5*width, [meds[sector][model.quarters[1]] for sector in meds], width, label=model.quarters[1])
q2 = ax.bar(x + 0.5*width, [meds[sector][model.quarters[2]] for sector in meds], width, label=model.quarters[2])
q3 = ax.bar(x + 1.5*width, [meds[sector][model.quarters[3]] for sector in meds], width, label=model.quarters[3])
ax.axhline(color='black')
ax.axhline(color='black')
for i in range(len(unique_sectors) - 1):
    ax.axvline(x=0.5 + i, linestyle='dashed', color='green')
ax.set_ylabel('Median Equity Change / EBITDA')
ax.set_title('Median Equity Change / EBITDA by Sector, Last 4 Quarters')
ax.set_xticks(x)
ax.set_xticklabels(unique_sectors)
fig.autofmt_xdate()
ax.legend()
plt.savefig('Equity Bar Charts/med_eq_tot_cng_ebitda_all.png')
