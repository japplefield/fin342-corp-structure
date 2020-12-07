import sys
sys.path.insert(1, 'handle_data/')
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
cur.execute("SELECT * FROM eq_cng_tot_ebd_2 INNER JOIN gics ON eq_cng_tot_ebd_2.symbol=gics.symbol WHERE gics.industry='Airlines'")
rows = cur.fetchall()
eq_cng_tot_ebd = {row['symbol']: {quarter: row[quarter] for quarter in model.quarters} for row in rows}
cur.execute("SELECT * FROM eq_cng_divs_ebd_2 INNER JOIN gics ON eq_cng_divs_ebd_2.symbol=gics.symbol WHERE gics.industry='Airlines'")
rows = cur.fetchall()
eq_cng_divs_ebd = {row['symbol']: {quarter: row[quarter] for quarter in model.quarters} for row in rows}
cur.execute("SELECT * FROM eq_cng_shares_ebd_2 INNER JOIN gics ON eq_cng_shares_ebd_2.symbol=gics.symbol WHERE gics.industry='Airlines'")
rows = cur.fetchall()
eq_cng_shares_ebd = {row['symbol']: {quarter: row[quarter] for quarter in model.quarters} for row in rows}
cur.execute("SELECT debt_cng_ebd.* FROM debt_cng_ebd INNER JOIN gics ON debt_cng_ebd.symbol=gics.symbol WHERE gics.industry='Airlines'")
rows = cur.fetchall()
debt_cng_ebd = {row['symbol']: {quarter: row[quarter] for quarter in model.quarters} for row in rows}

# Close Database
con.commit()

quarters = ['Q32019'] + list(model.quarters)
#Print Debt Change Line Graph by GICS sector
NUM_COLORS = len(debt_cng_ebd)
cm = plt.get_cmap('gist_rainbow')

# Airline debt Cumulative Line graph
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(5), quarters)
# plt.ylim(-0.3, 3)
for airline in debt_cng_ebd:
    plt.plot(range(5), [0] + [sum(list(debt_cng_ebd[airline].values())[:(i+1)]) for i in range(len(model.quarters))],  label=airline)
plt.xlabel('Quarter')
ax.axhline(color='black')
plt.ylabel('Cumulative Debt Change/Normalized EBITDA')
plt.title('Cumulative Debt Change/Normalized EBITDA for Airlines')
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('Airlines/airlines_debt_cng_ebitda_cum.png')

# Airline debt Cumulative Line graph
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(5), quarters)
# plt.ylim(-0.4, 0.6)
for airline in eq_cng_tot_ebd:
    plt.plot(range(5), [0] + [sum(list(eq_cng_tot_ebd[airline].values())[:(i+1)]) for i in range(len(model.quarters))],  label=airline)
plt.xlabel('Quarter')
ax.axhline(color='black')
plt.ylabel('Cumulative Equity Change/Normalized EBITDA')
plt.title('Cumulative Equity Change/Normalized EBITDA for Airlines')
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('Airlines/airlines_eq_tot_cng_ebitda_cum.png')

# Airline debt Cumulative Line graph
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(5), quarters)
# plt.ylim(-0.07, 0.02)
for airline in eq_cng_divs_ebd:
    plt.plot(range(5), [0] + [sum(list(eq_cng_divs_ebd[airline].values())[:(i+1)]) for i in range(len(model.quarters))],  label=airline)
plt.xlabel('Quarter')
ax.axhline(color='black')
plt.ylabel('Cumulative Equity Change from Dividends/Normalized EBITDA')
plt.title('Cumulative Equity Change from Dividends/Normalized EBITDA for Airlines')
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('Airlines/airlines_eq_divs_cng_ebitda_cum.png')

# Airline debt Cumulative Line graph
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(5), quarters)
# plt.ylim(-0.4, 0.6)
for airline in eq_cng_shares_ebd:
    plt.plot(range(5), [0] + [sum(list(eq_cng_shares_ebd[airline].values())[:(i+1)]) for i in range(len(model.quarters))],  label=airline)
plt.xlabel('Quarter')
ax.axhline(color='black')
plt.ylabel('Cumulative Equity Change from Share Issuance (Repurchase)/Normalized EBITDA')
plt.title('Cumulative Equity Change from Share Issuance (Repurchase)/Normalized EBITDA for Airlines')
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('Airlines/airlines_eq_shares_cng_ebitda_cum.png')


x = numpy.arange(len(debt_cng_ebd))
width = 0.2
fig, ax = plt.subplots()
q4 = ax.bar(x - 1.5*width, [debt_cng_ebd[airline][model.quarters[0]] for airline in debt_cng_ebd], width, label=model.quarters[0])
q1 = ax.bar(x - 0.5*width, [debt_cng_ebd[airline][model.quarters[1]] for airline in debt_cng_ebd], width, label=model.quarters[1])
q2 = ax.bar(x + 0.5*width, [debt_cng_ebd[airline][model.quarters[2]] for airline in debt_cng_ebd], width, label=model.quarters[2])
q3 = ax.bar(x + 1.5*width, [debt_cng_ebd[airline][model.quarters[3]] for airline in debt_cng_ebd], width, label=model.quarters[3])
ax.axhline(color='black')
ax.axhline(color='black')
for i in range(len(debt_cng_ebd) - 1):
    ax.axvline(x=0.5 + i, linestyle='dashed', color='green')
ax.set_ylabel('Airline Debt Change / EBITDA')
ax.set_title('Airline Debt Change / EBITDA Last 4 Quarters')
ax.set_xticks(x)
ax.set_xticklabels(debt_cng_ebd.keys())
ax.legend()
plt.savefig('Airlines/airlines_debt_cng_ebitda.png')

x = numpy.arange(len(eq_cng_tot_ebd))
width = 0.2
fig, ax = plt.subplots()
q4 = ax.bar(x - 1.5*width, [eq_cng_tot_ebd[airline][model.quarters[0]] for airline in eq_cng_tot_ebd], width, label=model.quarters[0])
q1 = ax.bar(x - 0.5*width, [eq_cng_tot_ebd[airline][model.quarters[1]] for airline in eq_cng_tot_ebd], width, label=model.quarters[1])
q2 = ax.bar(x + 0.5*width, [eq_cng_tot_ebd[airline][model.quarters[2]] for airline in eq_cng_tot_ebd], width, label=model.quarters[2])
q3 = ax.bar(x + 1.5*width, [eq_cng_tot_ebd[airline][model.quarters[3]] for airline in eq_cng_tot_ebd], width, label=model.quarters[3])
ax.axhline(color='black')
ax.axhline(color='black')
for i in range(len(eq_cng_tot_ebd) - 1):
    ax.axvline(x=0.5 + i, linestyle='dashed', color='green')
ax.set_ylabel('Airline Equity Change / EBITDA')
ax.set_title('Airline Equity Change / EBITDA Last 4 Quarters')
ax.set_xticks(x)
ax.set_xticklabels(eq_cng_tot_ebd.keys())
ax.legend()
plt.savefig('Airlines/airlines_eq_tot_cng_ebitda.png')

x = numpy.arange(len(eq_cng_divs_ebd))
width = 0.2
fig, ax = plt.subplots()
q4 = ax.bar(x - 1.5*width, [eq_cng_divs_ebd[airline][model.quarters[0]] for airline in eq_cng_divs_ebd], width, label=model.quarters[0])
q1 = ax.bar(x - 0.5*width, [eq_cng_divs_ebd[airline][model.quarters[1]] for airline in eq_cng_divs_ebd], width, label=model.quarters[1])
q2 = ax.bar(x + 0.5*width, [eq_cng_divs_ebd[airline][model.quarters[2]] for airline in eq_cng_divs_ebd], width, label=model.quarters[2])
q3 = ax.bar(x + 1.5*width, [eq_cng_divs_ebd[airline][model.quarters[3]] for airline in eq_cng_divs_ebd], width, label=model.quarters[3])
ax.axhline(color='black')
ax.axhline(color='black')
for i in range(len(eq_cng_divs_ebd) - 1):
    ax.axvline(x=0.5 + i, linestyle='dashed', color='green')
ax.set_ylabel('Airline Equity Change from Dividends / EBITDA')
ax.set_title('Airline Equity Change from Dividends / EBITDA Last 4 Quarters')
ax.set_xticks(x)
ax.set_xticklabels(eq_cng_divs_ebd.keys())
ax.legend()
plt.savefig('Airlines/airlines_eq_divs_cng_ebitda.png')

x = numpy.arange(len(eq_cng_shares_ebd))
width = 0.2
fig, ax = plt.subplots()
q4 = ax.bar(x - 1.5*width, [eq_cng_shares_ebd[airline][model.quarters[0]] for airline in eq_cng_shares_ebd], width, label=model.quarters[0])
q1 = ax.bar(x - 0.5*width, [eq_cng_shares_ebd[airline][model.quarters[1]] for airline in eq_cng_shares_ebd], width, label=model.quarters[1])
q2 = ax.bar(x + 0.5*width, [eq_cng_shares_ebd[airline][model.quarters[2]] for airline in eq_cng_shares_ebd], width, label=model.quarters[2])
q3 = ax.bar(x + 1.5*width, [eq_cng_shares_ebd[airline][model.quarters[3]] for airline in eq_cng_shares_ebd], width, label=model.quarters[3])
ax.axhline(color='black')
ax.axhline(color='black')
for i in range(len(eq_cng_shares_ebd) - 1):
    ax.axvline(x=0.5 + i, linestyle='dashed', color='green')
ax.set_ylabel('Airline Equity Change from Share Issuance (Repurchase) / EBITDA')
ax.set_title('Airline Equity Change from Share Issuance (Repurchase) / EBITDA Last 4 Quarters')
ax.set_xticks(x)
ax.set_xticklabels(eq_cng_shares_ebd.keys())
ax.legend()
plt.savefig('Airlines/airlines_eq_shares_cng_ebitda.png')
