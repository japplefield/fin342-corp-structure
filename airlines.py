import statistics
import model
import matplotlib.pyplot as plt
import numpy
from matplotlib import rcParams
from labellines import labelLine, labelLines

rcParams['figure.figsize'] = [15, 10]

con = model.sql_connection()
cur = con.cursor()

# Draw up For Airlines
cur.execute("SELECT * FROM eq_cng_ebd_2 INNER JOIN gics ON eq_cng_ebd_2.symbol=gics.symbol WHERE gics.industry='Airlines'")
rows = cur.fetchall()
airlines_eq_ebd_cng = {row['symbol']: {quarter: row[quarter] for quarter in model.quarters} for row in rows}
cur.execute("SELECT debt_cng_ebd.* FROM debt_cng_ebd INNER JOIN gics ON debt_cng_ebd.symbol=gics.symbol WHERE gics.industry='Airlines'")
rows = cur.fetchall()
airlines_debt_ebd_cng = {row['symbol']: {quarter: row[quarter] for quarter in model.quarters} for row in rows}

# Close Database
con.commit()

# Airline debt change graph
NUM_COLORS = len(airlines_debt_ebd_cng)
cm = plt.get_cmap('gist_rainbow')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(4), model.quarters)
plt.ylim(-0.3, 1.5)
for airline in airlines_debt_ebd_cng:
    plt.plot(range(4), [airlines_debt_ebd_cng[airline][quarter] for quarter in model.quarters],  label=airline)
plt.xlabel('Quarter')
plt.ylabel('Debt Change/Normalized EBITDA')
plt.title('Debt Change/Normalized EBITDA (Airlines)')
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('airline_debt_cng_ebitda_new.png')

# Airline equity change graph
NUM_COLORS = len(airlines_eq_ebd_cng)
cm = plt.get_cmap('gist_rainbow')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(4), model.quarters)
plt.ylim(-0.3, 0.85)
for airline in airlines_eq_ebd_cng:
    plt.plot(range(4), [airlines_eq_ebd_cng[airline][quarter] for quarter in model.quarters],  label=airline)
plt.xlabel('Quarter')
plt.ylabel('Equity Change/Normalized EBITDA')
plt.title('Equity Change/Normalized EBITDA (Airlines)')
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('airline_eq_cng_ebitda_new.png')
