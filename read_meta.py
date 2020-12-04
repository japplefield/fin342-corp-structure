import csv
import model
import statistics
# Read in each company's ticker and GICS classification info
def read_gics(cur):
    cur.execute("CREATE TABLE gics"
               "(symbol         TEXT UNIQUE, "
                "sector         TEXT, "
                "industry_group TEXT, "
                "industry       TEXT, "
                "sub_industry   TEXT );"
                )

    with open('SP1500GICS.csv', newline='', encoding='utf-8-sig') as ifh:
        reader = csv.DictReader(ifh)
        for row in reader:
            cur.execute("INSERT INTO gics(symbol, sector, industry_group, industry, sub_industry) "
                        "VALUES (?, ?, ?, ?, ?)", [row['Symbol'], row['GICS Sector'], row['GICS Industry Group'], row['GICS Industry'], row['GICS Sub-Industry']])

# Calculate Normalized EBITDA for each company
def read_ebitda(cur):
    cur.execute("CREATE TABLE ebitda"
               "(symbol      TEXT UNIQUE, "
                "mean_ebd FLOAT );"
                )
    with open('SP1500EBITDA.csv', newline='', encoding='utf-8-sig') as ifh:
        reader = csv.DictReader(ifh)
        for row in reader:
            row = model.strip_na(row)
            if len(row) == 1:
                continue
            cur.execute("INSERT INTO ebitda(symbol, mean_ebd) "
                        "VALUES (?, ?)", [row['Symbol'], statistics.mean([float(row[key]) for key in row if key != 'Symbol'])])
