#!/usr/bin/env python3
import sys
sys.path.insert(1, 'handle_data/')
import model
import statistics

con = model.sql_connection()
cur = con.cursor()

# Get GICS Unique sectors
cur.execute("SELECT DISTINCT sector FROM gics")
rows = cur.fetchall()
unique_sectors = [dct['sector'] for dct in rows]

med_sector_dbt_ebd_cng = {}
for sector in unique_sectors:
    cur.execute("SELECT * FROM debt_cng_ebd INNER JOIN gics ON debt_cng_ebd.symbol=gics.symbol WHERE gics.sector=?", [sector])
    rows = cur.fetchall()
    med_sector_dbt_ebd_cng[sector] = {quarter: statistics.median([row[quarter] for row in rows if row[quarter] is not None]) for quarter in model.quarters}

cur.execute("SELECT * FROM debt_cng_ebd ")
rows = cur.fetchall()
med_sector_dbt_ebd_cng['All'] = {quarter: statistics.median([row[quarter] for row in rows if row[quarter] is not None]) for quarter in model.quarters}

cur.execute("CREATE TABLE med_debt_cng_ebd "
                "(sector TEXT UNIQUE, "
                 "Q42019 FLOAT DEFAULT NULL, "
                 "Q12020 FLOAT DEFAULT NULL, "
                 "Q22020 FLOAT DEFAULT NULL, "
                 "Q32020 FLOAT DEFAULT NULL); ")

for sector in med_sector_dbt_ebd_cng:
    cur.execute("INSERT INTO med_debt_cng_ebd(sector, Q42019, Q12020, Q22020, Q32020) "
                "VALUES (?, ?, ?, ?, ?)", [sector] + list(med_sector_dbt_ebd_cng[sector].values()))




med_sector_eq_cng_divs_ebd = {}
for sector in unique_sectors:
    cur.execute("SELECT * FROM eq_cng_divs_ebd_2 INNER JOIN gics ON eq_cng_divs_ebd_2.symbol=gics.symbol WHERE gics.sector=?", [sector])
    rows = cur.fetchall()
    med_sector_eq_cng_divs_ebd[sector] = {quarter: statistics.median([row[quarter] for row in rows if row[quarter] is not None]) for quarter in model.quarters}

cur.execute("SELECT * FROM eq_cng_divs_ebd_2 ")
rows = cur.fetchall()
med_sector_eq_cng_divs_ebd['All'] = {quarter: statistics.median([row[quarter] for row in rows if row[quarter] is not None]) for quarter in model.quarters}

cur.execute("CREATE TABLE med_eq_cng_divs_ebd "
                "(sector TEXT UNIQUE, "
                 "Q42019 FLOAT DEFAULT NULL, "
                 "Q12020 FLOAT DEFAULT NULL, "
                 "Q22020 FLOAT DEFAULT NULL, "
                 "Q32020 FLOAT DEFAULT NULL); ")

for sector in med_sector_eq_cng_divs_ebd:
    cur.execute("INSERT INTO med_eq_cng_divs_ebd(sector, Q42019, Q12020, Q22020, Q32020) "
                "VALUES (?, ?, ?, ?, ?)", [sector] + list(med_sector_eq_cng_divs_ebd[sector].values()))




med_sector_eq_cng_shares_ebd = {}
for sector in unique_sectors:
    cur.execute("SELECT * FROM eq_cng_shares_ebd_2 INNER JOIN gics ON eq_cng_shares_ebd_2.symbol=gics.symbol WHERE gics.sector=?", [sector])
    rows = cur.fetchall()
    med_sector_eq_cng_shares_ebd[sector] = {quarter: statistics.median([row[quarter] for row in rows if row[quarter] is not None]) for quarter in model.quarters}

cur.execute("SELECT * FROM eq_cng_shares_ebd_2 ")
rows = cur.fetchall()
med_sector_eq_cng_shares_ebd['All'] = {quarter: statistics.median([row[quarter] for row in rows if row[quarter] is not None]) for quarter in model.quarters}

cur.execute("CREATE TABLE med_eq_cng_shares_ebd "
                "(sector TEXT UNIQUE, "
                 "Q42019 FLOAT DEFAULT NULL, "
                 "Q12020 FLOAT DEFAULT NULL, "
                 "Q22020 FLOAT DEFAULT NULL, "
                 "Q32020 FLOAT DEFAULT NULL); ")

for sector in med_sector_eq_cng_shares_ebd:
    cur.execute("INSERT INTO med_eq_cng_shares_ebd(sector, Q42019, Q12020, Q22020, Q32020) "
                "VALUES (?, ?, ?, ?, ?)", [sector] + list(med_sector_eq_cng_shares_ebd[sector].values()))




med_sector_eq_cng_tot_ebd = {}
for sector in unique_sectors:
    cur.execute("SELECT * FROM eq_cng_tot_ebd_2 INNER JOIN gics ON eq_cng_tot_ebd_2.symbol=gics.symbol WHERE gics.sector=?", [sector])
    rows = cur.fetchall()
    med_sector_eq_cng_tot_ebd[sector] = {quarter: statistics.median([row[quarter] for row in rows if row[quarter] is not None]) for quarter in model.quarters}

cur.execute("SELECT * FROM eq_cng_tot_ebd_2 ")
rows = cur.fetchall()
med_sector_eq_cng_tot_ebd['All'] = {quarter: statistics.median([row[quarter] for row in rows if row[quarter] is not None]) for quarter in model.quarters}

cur.execute("CREATE TABLE med_eq_cng_tot_ebd "
                "(sector TEXT UNIQUE, "
                 "Q42019 FLOAT DEFAULT NULL, "
                 "Q12020 FLOAT DEFAULT NULL, "
                 "Q22020 FLOAT DEFAULT NULL, "
                 "Q32020 FLOAT DEFAULT NULL); ")

for sector in med_sector_eq_cng_tot_ebd:
    cur.execute("INSERT INTO med_eq_cng_tot_ebd(sector, Q42019, Q12020, Q22020, Q32020) "
                "VALUES (?, ?, ?, ?, ?)", [sector] + list(med_sector_eq_cng_tot_ebd[sector].values()))





med_sector_tot_debt_eq_cng_ebd = {}

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
    med_sector_tot_debt_eq_cng_ebd[sector] = {quarter: statistics.median([row[quarter] for row in rows if row[quarter] is not None]) for quarter in model.quarters}

cur.execute("SELECT     debt_cng_ebd.Q42019 + eq_cng_tot_ebd_2.Q42019 AS Q42019, "
            "debt_cng_ebd.Q12020 + eq_cng_tot_ebd_2.Q12020 AS Q12020, "
            "debt_cng_ebd.Q22020 + eq_cng_tot_ebd_2.Q22020 AS Q22020, "
            "debt_cng_ebd.Q32020 + eq_cng_tot_ebd_2.Q32020 AS Q32020 "
            "FROM       debt_cng_ebd "
            "INNER JOIN eq_cng_tot_ebd_2 "
            "ON        debt_cng_ebd.symbol=eq_cng_tot_ebd_2.symbol")
rows = cur.fetchall()
med_sector_tot_debt_eq_cng_ebd['All'] = {quarter: statistics.median([row[quarter] for row in rows if row[quarter] is not None]) for quarter in model.quarters}


cur.execute("CREATE TABLE med_tot_eq_debt_cng_ebd "
                "(sector TEXT UNIQUE, "
                 "Q42019 FLOAT DEFAULT NULL, "
                 "Q12020 FLOAT DEFAULT NULL, "
                 "Q22020 FLOAT DEFAULT NULL, "
                 "Q32020 FLOAT DEFAULT NULL); ")


for sector in med_sector_eq_cng_tot_ebd:
    cur.execute("INSERT INTO med_tot_eq_debt_cng_ebd(sector, Q42019, Q12020, Q22020, Q32020) "
                "VALUES (?, ?, ?, ?, ?)", [sector] + list(med_sector_tot_debt_eq_cng_ebd[sector].values()))

con.commit()
