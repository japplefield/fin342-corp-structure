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
