import csv
# Read in Debt info for each company and calculate change in debt
def read_debt(cur):
    cur.execute("CREATE TABLE debt"
                "(symbol TEXT UNIQUE, "
                 "Q32019 FLOAT DEFAULT NULL, "
                 "Q42019 FLOAT DEFAULT NULL, "
                 "Q12020 FLOAT DEFAULT NULL, "
                 "Q22020 FLOAT DEFAULT NULL, "
                 "Q32020 FLOAT DEFAULT NULL); ")

    with open('SP1500Debt.csv', newline='', encoding='utf-8-sig') as ifh:
        reader = csv.DictReader(ifh)
        for row in reader:
            vals = list(row.values())
            for i in range(len(vals)):
                if vals[i] == '' or vals[i] == '#N/A':
                    vals[i] = None
            cur.execute("INSERT INTO debt(symbol, Q32019, Q42019, Q12020, Q22020, Q32020) "
                        "VALUES (?, ?, ?, ?, ?, ?)", vals)


    cur.execute("CREATE TABLE debt_cng"
                "(symbol TEXT UNIQUE, "
                "Q42019 FLOAT DEFAULT NULL, "
                "Q12020 FLOAT DEFAULT NULL, "
                "Q22020 FLOAT DEFAULT NULL, "
                "Q32020 FLOAT DEFAULT NULL);")

    cur.execute("SELECT * from debt")
    rows = cur.fetchall()
    for row in rows:
        if None in row.values():
            continue
        cur.execute("INSERT INTO debt_cng(symbol, Q42019, Q12020, Q22020, Q32020) "
                    "VALUES (?, ?, ?, ?, ?)", [row['symbol'], row['Q42019'] - row['Q32019'], row['Q12020'] - row['Q42019'], row['Q22020'] - row['Q12020'], row['Q32020'] - row['Q22020']])

# Calculate Cng Debt / Normalized EBITDA for the 4 periods
def cng_dbt_ebd(cur):
    cur.execute("CREATE TABLE debt_cng_ebd"
                "(symbol TEXT UNIQUE, "
                "Q42019 FLOAT DEFAULT NULL, "
                "Q12020 FLOAT DEFAULT NULL, "
                "Q22020 FLOAT DEFAULT NULL, "
                "Q32020 FLOAT DEFAULT NULL);")

    cur.execute("SELECT * FROM debt_cng INNER JOIN ebitda ON debt_cng.symbol=ebitda.symbol")
    rows = cur.fetchall()
    for row in rows:
        cur.execute("INSERT INTO debt_cng_ebd(symbol, Q42019, Q12020, Q22020, Q32020) "
                    "VALUES (?, ?, ?, ?, ?)", [row['symbol'], row['Q42019'] / row['mean_ebd'], row['Q12020'] / row['mean_ebd'], row['Q22020'] / row['mean_ebd'], row['Q32020'] / row['mean_ebd']])
