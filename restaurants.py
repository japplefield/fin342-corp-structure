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



# Draw up For restaurants
cur.execute("SELECT * FROM eq_cng_tot_ebd_2 INNER JOIN gics ON eq_cng_tot_ebd_2.symbol=gics.symbol WHERE gics.sub_industry='Restaurants'")
rows = cur.fetchall()
res = {row['symbol']: {quarter: row[quarter] for quarter in model.quarters} for row in rows}
eq_cng_tot_ebd = {restaurant: res[restaurant] for restaurant in res if None not in res[restaurant].values()}
cur.execute("SELECT * FROM eq_cng_divs_ebd_2 INNER JOIN gics ON eq_cng_divs_ebd_2.symbol=gics.symbol WHERE gics.sub_industry='Restaurants'")
rows = cur.fetchall()
res = {row['symbol']: {quarter: row[quarter] for quarter in model.quarters} for row in rows}
eq_cng_divs_ebd = {restaurant: res[restaurant] for restaurant in res if None not in res[restaurant].values()}
cur.execute("SELECT * FROM eq_cng_shares_ebd_2 INNER JOIN gics ON eq_cng_shares_ebd_2.symbol=gics.symbol WHERE gics.sub_industry='Restaurants'")
rows = cur.fetchall()
res = {row['symbol']: {quarter: row[quarter] for quarter in model.quarters} for row in rows}
eq_cng_shares_ebd = {restaurant: res[restaurant] for restaurant in res if None not in res[restaurant].values()}
cur.execute("SELECT debt_cng_ebd.* FROM debt_cng_ebd INNER JOIN gics ON debt_cng_ebd.symbol=gics.symbol WHERE gics.sub_industry='Restaurants'")
rows = cur.fetchall()
res = {row['symbol']: {quarter: row[quarter] for quarter in model.quarters} for row in rows}
debt_cng_ebd = {restaurant: res[restaurant] for restaurant in res if None not in res[restaurant].values()}

# Close Database
con.commit()

quarters = ['Q32019'] + list(model.quarters)
#Print Debt Change Line Graph by GICS sector
NUM_COLORS = len(debt_cng_ebd)
cm = plt.get_cmap('gist_rainbow')

# restaurant debt Cumulative Line graph
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(5), quarters)
# plt.ylim(-0.3, 3)
for restaurant in debt_cng_ebd:
    plt.plot(range(5), [0] + [sum(list(debt_cng_ebd[restaurant].values())[:(i+1)]) for i in range(len(model.quarters))],  label=restaurant)
plt.xlabel('Quarter')
ax.axhline(color='black')
plt.ylabel('Cumulative Debt Change/Normalized EBITDA')
plt.title('Cumulative Debt Change/Normalized EBITDA for Restaurants')
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('Restaurants/restaurants_debt_cng_ebitda_cum.png')

# restaurant debt Cumulative Line graph
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(5), quarters)
# plt.ylim(-0.4, 0.6)
for restaurant in eq_cng_tot_ebd:
    plt.plot(range(5), [0] + [sum(list(eq_cng_tot_ebd[restaurant].values())[:(i+1)]) for i in range(len(model.quarters))],  label=restaurant)
plt.xlabel('Quarter')
ax.axhline(color='black')
plt.ylabel('Cumulative Equity Change/Normalized EBITDA')
plt.title('Cumulative Equity Change/Normalized EBITDA for Restaurants')
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('Restaurants/restaurants_eq_tot_cng_ebitda_cum.png')

# restaurant debt Cumulative Line graph
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(5), quarters)
# plt.ylim(-0.07, 0.02)
for restaurant in eq_cng_divs_ebd:
    plt.plot(range(5), [0] + [sum(list(eq_cng_divs_ebd[restaurant].values())[:(i+1)]) for i in range(len(model.quarters))],  label=restaurant)
plt.xlabel('Quarter')
ax.axhline(color='black')
plt.ylabel('Cumulative Equity Change from Dividends/Normalized EBITDA')
plt.title('Cumulative Equity Change from Dividends/Normalized EBITDA for Restaurants')
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('Restaurants/restaurants_eq_divs_cng_ebitda_cum.png')

# restaurant debt Cumulative Line graph
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(5), quarters)
# plt.ylim(-0.4, 0.6)
for restaurant in eq_cng_shares_ebd:
    plt.plot(range(5), [0] + [sum(list(eq_cng_shares_ebd[restaurant].values())[:(i+1)]) for i in range(len(model.quarters))],  label=restaurant)
plt.xlabel('Quarter')
ax.axhline(color='black')
plt.ylabel('Cumulative Equity Change from Share Issuance (Repurchase)/Normalized EBITDA')
plt.title('Cumulative Equity Change from Share Issuance (Repurchase)/Normalized EBITDA for Restaurants')
plt.tight_layout()
labelLines(plt.gca().get_lines())
plt.savefig('Restaurants/restaurants_eq_shares_cng_ebitda_cum.png')


x = numpy.arange(len(debt_cng_ebd))
width = 0.2
fig, ax = plt.subplots()
q4 = ax.bar(x - 1.5*width, [debt_cng_ebd[restaurant][model.quarters[0]] for restaurant in debt_cng_ebd], width, label=model.quarters[0])
q1 = ax.bar(x - 0.5*width, [debt_cng_ebd[restaurant][model.quarters[1]] for restaurant in debt_cng_ebd], width, label=model.quarters[1])
q2 = ax.bar(x + 0.5*width, [debt_cng_ebd[restaurant][model.quarters[2]] for restaurant in debt_cng_ebd], width, label=model.quarters[2])
q3 = ax.bar(x + 1.5*width, [debt_cng_ebd[restaurant][model.quarters[3]] for restaurant in debt_cng_ebd], width, label=model.quarters[3])
ax.axhline(color='black')
ax.axhline(color='black')
for i in range(len(debt_cng_ebd) - 1):
    ax.axvline(x=0.5 + i, linestyle='dashed', color='green')
ax.set_ylabel('Restaurant Debt Change / EBITDA')
ax.set_title('Restaurant Debt Change / EBITDA Last 4 Quarters')
ax.set_xticks(x)
ax.set_xticklabels(debt_cng_ebd.keys())
ax.legend()
plt.savefig('Restaurants/restaurants_debt_cng_ebitda.png')

x = numpy.arange(len(eq_cng_tot_ebd))
width = 0.2
fig, ax = plt.subplots()
q4 = ax.bar(x - 1.5*width, [eq_cng_tot_ebd[restaurant][model.quarters[0]] for restaurant in eq_cng_tot_ebd], width, label=model.quarters[0])
q1 = ax.bar(x - 0.5*width, [eq_cng_tot_ebd[restaurant][model.quarters[1]] for restaurant in eq_cng_tot_ebd], width, label=model.quarters[1])
q2 = ax.bar(x + 0.5*width, [eq_cng_tot_ebd[restaurant][model.quarters[2]] for restaurant in eq_cng_tot_ebd], width, label=model.quarters[2])
q3 = ax.bar(x + 1.5*width, [eq_cng_tot_ebd[restaurant][model.quarters[3]] for restaurant in eq_cng_tot_ebd], width, label=model.quarters[3])
ax.axhline(color='black')
ax.axhline(color='black')
for i in range(len(eq_cng_tot_ebd) - 1):
    ax.axvline(x=0.5 + i, linestyle='dashed', color='green')
ax.set_ylabel('Restaurant Equity Change / EBITDA')
ax.set_title('Restaurant Equity Change / EBITDA Last 4 Quarters')
ax.set_xticks(x)
ax.set_xticklabels(eq_cng_tot_ebd.keys())
ax.legend()
plt.savefig('Restaurants/restaurants_eq_tot_cng_ebitda.png')

x = numpy.arange(len(eq_cng_divs_ebd))
width = 0.2
fig, ax = plt.subplots()
q4 = ax.bar(x - 1.5*width, [eq_cng_divs_ebd[restaurant][model.quarters[0]] for restaurant in eq_cng_divs_ebd], width, label=model.quarters[0])
q1 = ax.bar(x - 0.5*width, [eq_cng_divs_ebd[restaurant][model.quarters[1]] for restaurant in eq_cng_divs_ebd], width, label=model.quarters[1])
q2 = ax.bar(x + 0.5*width, [eq_cng_divs_ebd[restaurant][model.quarters[2]] for restaurant in eq_cng_divs_ebd], width, label=model.quarters[2])
q3 = ax.bar(x + 1.5*width, [eq_cng_divs_ebd[restaurant][model.quarters[3]] for restaurant in eq_cng_divs_ebd], width, label=model.quarters[3])
ax.axhline(color='black')
ax.axhline(color='black')
for i in range(len(eq_cng_divs_ebd) - 1):
    ax.axvline(x=0.5 + i, linestyle='dashed', color='green')
ax.set_ylabel('Restaurant Equity Change from Dividends / EBITDA')
ax.set_title('Restaurant Equity Change from Dividends / EBITDA Last 4 Quarters')
ax.set_xticks(x)
ax.set_xticklabels(eq_cng_divs_ebd.keys())
ax.legend()
plt.savefig('Restaurants/restaurants_eq_divs_cng_ebitda.png')

x = numpy.arange(len(eq_cng_shares_ebd))
width = 0.2
fig, ax = plt.subplots()
q4 = ax.bar(x - 1.5*width, [eq_cng_shares_ebd[restaurant][model.quarters[0]] for restaurant in eq_cng_shares_ebd], width, label=model.quarters[0])
q1 = ax.bar(x - 0.5*width, [eq_cng_shares_ebd[restaurant][model.quarters[1]] for restaurant in eq_cng_shares_ebd], width, label=model.quarters[1])
q2 = ax.bar(x + 0.5*width, [eq_cng_shares_ebd[restaurant][model.quarters[2]] for restaurant in eq_cng_shares_ebd], width, label=model.quarters[2])
q3 = ax.bar(x + 1.5*width, [eq_cng_shares_ebd[restaurant][model.quarters[3]] for restaurant in eq_cng_shares_ebd], width, label=model.quarters[3])
ax.axhline(color='black')
ax.axhline(color='black')
for i in range(len(eq_cng_shares_ebd) - 1):
    ax.axvline(x=0.5 + i, linestyle='dashed', color='green')
ax.set_ylabel('Restaurant Equity Change from Share Issuance (Repurchase) / EBITDA')
ax.set_title('Restaurant Equity Change from Share Issuance (Repurchase) / EBITDA Last 4 Quarters')
ax.set_xticks(x)
ax.set_xticklabels(eq_cng_shares_ebd.keys())
ax.legend()
plt.savefig('Restaurants/restaurants_eq_shares_cng_ebitda.png')
