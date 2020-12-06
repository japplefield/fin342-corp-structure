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

# Calculate Summary Median Eq Cng / EBITDA for each sector
for sector in unique_sectors:
    cur.execute("SELECT * FROM eq_cng_tot_ebd_2 INNER JOIN gics ON eq_cng_tot_ebd_2.symbol=gics.symbol WHERE gics.sector=?", [sector])
    rows = cur.fetchall()
    meds = [statistics.median([row[quarter] for row in rows if row[quarter] is not None]) for quarter in model.quarters]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.bar(numpy.arange(len(meds)), meds, align='center', color='blue')
    plt.xlabel('Quarter')
    plt.ylabel('Median Equity Change / Normalized EBITDA')
    plt.title(f'Median Quarterly Equity Change / Normalized EBITDA for {sector}')
    plt.xticks(numpy.arange(len(meds)), model.quarters)
    plt.ylim(-0.1, 0.015)
    ax = plt.gca()
    ax.spines["bottom"].set_position(("data", 0))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.savefig(f'Equity Bar Charts/med_eq_cng_ebitda_{sector}.png')



# Close Database
con.commit()
