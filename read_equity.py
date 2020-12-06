import csv
from datetime import datetime, timedelta
import statistics
#Calculate Average price for each quarter for each firm
def read_prices(cur):
    Q419ST = datetime.strptime("10/01/2019", "%m/%d/%Y")
    Q120ST = datetime.strptime("01/01/2020", "%m/%d/%Y")
    Q220ST = datetime.strptime("04/01/2020", "%m/%d/%Y")
    Q320ST = datetime.strptime("07/01/2020", "%m/%d/%Y")
    Q420ST = datetime.strptime("10/01/2020", "%m/%d/%Y")

    cur.execute("CREATE TABLE avg_price"
                "(symbol TEXT UNIQUE, "
                "Q32019 FLOAT DEFAULT NULL, "
                "Q42019 FLOAT DEFAULT NULL, "
                "Q12020 FLOAT DEFAULT NULL, "
                "Q22020 FLOAT DEFAULT NULL, "
                "Q32020 FLOAT DEFAULT NULL);")

    with open('SP1500DatedPrices.csv', newline='', encoding='utf-8-sig') as ifh:
        reader = csv.DictReader(ifh)
        for row in reader:
            if '#N/A' in row.values():
                continue
            ticker = row['Symbol']
            Q319AvgP = statistics.mean([ float(row[date]) for date in reader.fieldnames[1:]  if datetime.strptime(date, "%m/%d/%Y") < Q419ST ])
            Q419AvgP = statistics.mean([ float(row[date]) for date in reader.fieldnames[1:]  if datetime.strptime(date, "%m/%d/%Y") < Q120ST ])
            Q120AvgP = statistics.mean([ float(row[date]) for date in reader.fieldnames[1:]  if datetime.strptime(date, "%m/%d/%Y") < Q220ST ])
            Q220AvgP = statistics.mean([ float(row[date]) for date in reader.fieldnames[1:]  if datetime.strptime(date, "%m/%d/%Y") < Q320ST ])
            Q320AvgP = statistics.mean([ float(row[date]) for date in reader.fieldnames[1:]  if datetime.strptime(date, "%m/%d/%Y") < Q420ST ])
            cur.execute("INSERT INTO avg_price(symbol, Q32019, Q42019, Q12020, Q22020, Q32020) "
                        "VALUES (?, ?, ?, ?, ?, ?)", [ticker, Q319AvgP, Q419AvgP, Q120AvgP, Q220AvgP, Q320AvgP])


# Read in Data on Shares Outstanding
def read_shares(cur):
    cur.execute("CREATE TABLE shares"
                "(symbol TEXT UNIQUE, "
                "Q32019 FLOAT DEFAULT NULL, "
                "Q42019 FLOAT DEFAULT NULL, "
                "Q12020 FLOAT DEFAULT NULL, "
                "Q22020 FLOAT DEFAULT NULL, "
                "Q32020 FLOAT DEFAULT NULL);")

    with open('SP1500SharesOutstanding.csv', newline='', encoding='utf-8-sig') as ifh:
        reader = csv.DictReader(ifh)
        for row in reader:
            vals = list(row.values())
            if '#N/A' in vals:
                continue
            for i in range(len(vals)):
                if vals[i] == '':
                    vals[i] = None
            cur.execute("INSERT INTO shares(symbol, Q32019, Q42019, Q12020, Q22020, Q32020) "
                        "VALUES (?, ?, ?, ?, ?, ?)", vals)


def read_dividends(cur):
    cur.execute("CREATE TABLE dividends"
                "(symbol TEXT UNIQUE, "
                "Q32019 FLOAT DEFAULT NULL, "
                "Q42019 FLOAT DEFAULT NULL, "
                "Q12020 FLOAT DEFAULT NULL, "
                "Q22020 FLOAT DEFAULT NULL, "
                "Q32020 FLOAT DEFAULT NULL);")

    with open('SP1500DividendsPerShare.csv', newline='', encoding='utf-8-sig') as ifh:
        reader = csv.DictReader(ifh)
        for row in reader:
            vals = list(row.values())
            for i in range(len(vals)):
                if vals[i] == '#N/A':
                    vals[i] = 0
                if vals[i] == '':
                    vals[i] = None
            cur.execute("INSERT INTO dividends(symbol, Q32019, Q42019, Q12020, Q22020, Q32020) "
                        "VALUES (?, ?, ?, ?, ?, ?)", vals)

# Calculate absolute change in equity for each quarter, with and without dividends
def calc_eq_cng(cur):
    cur.execute("CREATE TABLE eq_cng_shares"
                "(symbol TEXT, "
                "period TEXT DEFAULT NULL, "
                "change FLOAT DEFAULT NULL);")

    quarters = ['Q32019', 'Q42019', 'Q12020', 'Q22020', 'Q32020']
    for i in range(1, len(quarters)):
        q = ("SELECT avg_price.symbol, "
            "avg_price.{} AS p, "
            "shares.{} AS s1, shares.{} AS s2 "
            "FROM avg_price, shares "
            "WHERE avg_price.symbol=shares.symbol").format(*tuple([quarters[i]] + quarters[i-1:i+1]))
        cur.execute(q)
        rows = cur.fetchall()
        for row in rows:
            if None in row.values():
                continue
            eq_cng = row['p'] * (row['s2'] - row['s1'])
            cur.execute("INSERT INTO eq_cng_shares(symbol, period, change) "
                        "VALUES (?, ?, ?)", [row['symbol'], quarters[i], eq_cng])

    cur.execute("CREATE TABLE eq_cng_divs"
                "(symbol TEXT, "
                "period TEXT DEFAULT NULL, "
                "change FLOAT DEFAULT NULL);")

    quarters = ['Q42019', 'Q12020', 'Q22020', 'Q32020']
    for i in range(len(quarters)):
        q = ("SELECT avg_price.symbol, "
            "avg_price.{} AS p, "
            "shares.{} AS s, "
            "dividends.{} AS d "
            "FROM avg_price, shares, dividends "
            "WHERE avg_price.symbol=shares.symbol AND shares.symbol=dividends.symbol ").format(quarters[i], quarters[i], quarters[i])
        cur.execute(q)
        rows = cur.fetchall()
        for row in rows:
            if None in row.values():
                continue
            eq_cng = -1 * row['d'] * row['s']
            cur.execute("INSERT INTO eq_cng_divs(symbol, period, change) "
                        "VALUES (?, ?, ?)", [row['symbol'], quarters[i], eq_cng])

# Calculate normalized change in equity (dividends and share changes) by mean EBITDA
def calc_eq_cng_ebd(cur):
    cur.execute("CREATE TABLE eq_cng_shares_ebd"
                "(symbol TEXT, "
                "period TEXT DEFAULT NULL, "
                "change FLOAT DEFAULT NULL);")

    cur.execute("SELECT * from eq_cng_shares INNER JOIN ebitda ON eq_cng_shares.symbol = ebitda.symbol")
    rows = cur.fetchall()
    for row in rows:
        cur.execute("INSERT INTO eq_cng_shares_ebd(symbol, period, change) "
                    "VALUES (?, ?, ?)", [row['symbol'], row['period'], row['change'] / row['mean_ebd']])

    cur.execute("CREATE TABLE eq_cng_divs_ebd"
                "(symbol TEXT, "
                "period TEXT DEFAULT NULL, "
                "change FLOAT DEFAULT NULL);")

    cur.execute("SELECT * from eq_cng_divs INNER JOIN ebitda ON eq_cng_divs.symbol = ebitda.symbol")
    rows = cur.fetchall()
    for row in rows:
        cur.execute("INSERT INTO eq_cng_divs_ebd(symbol, period, change) "
                    "VALUES (?, ?, ?)", [row['symbol'], row['period'], row['change'] / row['mean_ebd']])

    cur.execute("CREATE TABLE eq_cng_tot_ebd"
                "(symbol TEXT, "
                "period TEXT DEFAULT NULL, "
                "change FLOAT DEFAULT NULL);")

    cur.execute("SELECT eq_cng_divs_ebd.symbol, eq_cng_divs_ebd.period, eq_cng_divs_ebd.change AS d, eq_cng_shares_ebd.change AS s "
                "FROM eq_cng_divs_ebd INNER JOIN eq_cng_shares_ebd "
                "ON eq_cng_divs_ebd.symbol=eq_cng_shares_ebd.symbol AND eq_cng_divs_ebd.period=eq_cng_shares_ebd.period")
    rows = cur.fetchall()
    for row in rows:
        cur.execute("INSERT INTO eq_cng_tot_ebd(symbol, period, change) "
                    "VALUES (?, ?, ?)", [row['symbol'], row['period'], row['d'] + row['s']])

def eq_cng_ebd_refactor(cur):
    cur.execute("CREATE TABLE eq_cng_shares_ebd_2"
                "(symbol TEXT UNIQUE, "
                "Q42019 FLOAT DEFAULT NULL, "
                "Q12020 FLOAT DEFAULT NULL, "
                "Q22020 FLOAT DEFAULT NULL, "
                "Q32020 FLOAT DEFAULT NULL);")

    cur.execute("SELECT symbol FROM eq_cng_shares_ebd")
    symbols = set([row['symbol'] for row in cur.fetchall()])
    for symbol in symbols:
        cur.execute("SELECT * FROM eq_cng_shares_ebd WHERE symbol=?", [symbol])
        rows = cur.fetchall()
        changes = {row['period']: row['change'] for row in rows}
        quarters = ['Q42019', 'Q12020', 'Q22020', 'Q32020']
        for quarter in quarters:
            if quarter not in changes:
                changes[quarter] = None
        cur.execute("INSERT INTO eq_cng_shares_ebd_2(symbol, Q42019, Q12020, Q22020, Q32020) "
                    "VALUES (?, ?, ?, ?, ?)", [symbol] + [changes[quarter] for quarter in quarters])

    cur.execute("CREATE TABLE eq_cng_divs_ebd_2"
                "(symbol TEXT UNIQUE, "
                "Q42019 FLOAT DEFAULT NULL, "
                "Q12020 FLOAT DEFAULT NULL, "
                "Q22020 FLOAT DEFAULT NULL, "
                "Q32020 FLOAT DEFAULT NULL);")

    cur.execute("SELECT symbol FROM eq_cng_divs_ebd")
    symbols = set([row['symbol'] for row in cur.fetchall()])
    for symbol in symbols:
        cur.execute("SELECT * FROM eq_cng_divs_ebd WHERE symbol=?", [symbol])
        rows = cur.fetchall()
        changes = {row['period']: row['change'] for row in rows}
        quarters = ['Q42019', 'Q12020', 'Q22020', 'Q32020']
        for quarter in quarters:
            if quarter not in changes:
                changes[quarter] = None
        cur.execute("INSERT INTO eq_cng_divs_ebd_2(symbol, Q42019, Q12020, Q22020, Q32020) "
                    "VALUES (?, ?, ?, ?, ?)", [symbol] + [changes[quarter] for quarter in quarters])

    cur.execute("CREATE TABLE eq_cng_tot_ebd_2"
                "(symbol TEXT UNIQUE, "
                "Q42019 FLOAT DEFAULT NULL, "
                "Q12020 FLOAT DEFAULT NULL, "
                "Q22020 FLOAT DEFAULT NULL, "
                "Q32020 FLOAT DEFAULT NULL);")

    cur.execute("SELECT symbol FROM eq_cng_tot_ebd")
    symbols = set([row['symbol'] for row in cur.fetchall()])
    for symbol in symbols:
        cur.execute("SELECT * FROM eq_cng_tot_ebd WHERE symbol=?", [symbol])
        rows = cur.fetchall()
        changes = {row['period']: row['change'] for row in rows}
        quarters = ['Q42019', 'Q12020', 'Q22020', 'Q32020']
        for quarter in quarters:
            if quarter not in changes:
                changes[quarter] = None
        cur.execute("INSERT INTO eq_cng_tot_ebd_2(symbol, Q42019, Q12020, Q22020, Q32020) "
                    "VALUES (?, ?, ?, ?, ?)", [symbol] + [changes[quarter] for quarter in quarters])
