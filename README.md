# Pandemic Induced Restructuring
## Justin Applefield
## FIN 342: Big Data in Finance
## December 8, 2020

## Table of Contents
* [Introduction](#introduction)
* [Data](#data)
* [Technologies](#technologies)
* [Methodology](#methodology)
* [Results](#results)
* [Appendix A: Sample Code](#appendix-a-sample-code)
* [Appendix B: Setup](#appendix-b-setup)

## Introduction
In early 2020, markets took a huge dive as the COVID-19 pandemic worsened. Uncertainty has led to lots of cost cutting, but what will the actual effect be on corporations’ ability to pay off their debt? On the other hand, low interest rates might lead companies to try to acquire more debt for cheap. What is the net effect these two conflicting trends might have on corporate structure and debt levels, and how does this vary by industry? An analysis will help understand a lot about how each industry is affected by things like consumer trends and the Fed’s policies, and may provide some future insight about what industries may be exposed to higher leverage risk going forward.

## Data
The data set comprises of S&P 1500 companies’ balance sheets and debt schedules pre-COVID-19 and currently. The S&P 1500 was chosen because it covers approximately 90% of the total market capitalization of US stocks, and is therefore representative of the US market as a whole. Data was retrieved from FactSet. The firm-by-firm data include:

* Debt during each of the past five quarters and EBITDA on an historical, annual basis over a few years ending December 2019 for all available firms
* Quarterly dividends per share from Q4 2019 to Q3 2020 for all available firms
* Share price every day from October 1, 2019 to September 30, 2020 for all available firms
* Quarterly shares outstanding from Q4 2019 to Q3 2020 for all available firms
* GICS classification meta-data for all S&P 1500 companies

Because only data where all this information were available for a given firm was usable, the final data set included only 1322 firms, as opposed to the 1500 in the S&P 1500. The majority of this discrepancy is attributable to firms where none of the past five years' EBITDA information was available on FactSet, so those firms were excluded from the sample.

## Methodology
I computed a normalized EBITDA using 2015-2019 annual EBITDA for each company. I then computed Total Debt/normalized EBITDA for each company at December 31, 2019, March 31, 2020, June 30, 2020 and September 30, 2020. Then, I computed industry median Debt/normalized EBITDA over these 4 estimation dates to describe how industry leverage has changed over the COVID-19 window. Next, I computed an average share price for each company for each quarter in study, and determined the total equity value raised or returned to shareholders as a result of:

* Share issuance or buybacks (assuming these all occurred at the average share price that quarter)
* Dividend payment

An extension to this analysis would be to determine whether there is a relationship between corporate bond yields and leverage changes (for example, does the data show reductions in leverage during quarters when corporate bond yields increased, and increases in leverage during quarters when corporate bond yields decreased; and if industry corporate bond yields are available, are changes in corporate bond yields by industry associated with changes in leverage by industry). This analysis was not performed during the course of this project.

## Technologies
Python was used to handle all data management and graph generation. The relational database management system used was SQLite, as it is included in the Python Standard Library. For graph generation, Matplotlib and NumPy were used. [Github user cphyc's project matplotlib-label-lines](https://github.com/cphyc/matplotlib-label-lines) was also used to make some of the graphs more readable.

Sample SQL and Python code can be found in [Appendix A](#appendix-a-sample-code).


## Results





## Appendix A: Sample Code

### Sample Database Schema
The following is an example of the database schema used to store final change in debt to normalized EBITDA ratios used:
```SQL
CREATE TABLE debt_cng_ebd
  (
     symbol TEXT UNIQUE,
     q42019 FLOAT DEFAULT NULL,
     q12020 FLOAT DEFAULT NULL,
     q22020 FLOAT DEFAULT NULL,
     q32020 FLOAT DEFAULT NULL
  );
```
A similar structure was used for the change in equity to normalized EBITDA ratios, change in equity attributable to dividends paid to normalized EBITDA ratios, and change in equity attributable to share repurchase (issuance) to normalized EBITDA ratios.

### Sample Database Query
The following is an example of the python code used to retrieve the median debt change to normalized EBITDA ratio for each GICS sector. A similar code fragment was used for other database queries.
```python
for sector in unique_sectors:
    cur.execute("SELECT * "
                "FROM   debt_cng_ebd "
                "       INNER JOIN gics "
                "       ON debt_cng_ebd.symbol = gics.symbol "
                "WHERE gics.sector=?", [sector])
    rows = cur.fetchall()
    meds[sector] = {quarter: statistics.median([row[quarter]
                                                for row in rows
                                                if row[quarter] is not None])
                    for quarter in model.quarters}
```
The above Python code has an embedded SQL query. Here is just that query alone:
```SQL
SELECT *
FROM   debt_cng_ebd
       INNER JOIN gics
               ON debt_cng_ebd.symbol = gics.symbol
WHERE  gics.sector = industrials
```

### Sample Bar Chart Generation
The following is an example of the Python code that uses Matplotlib to generate a bar chart showing the median debt change to normalized EBTIDA for each GICS sector for each quarter in study. Similar code was used for other bar charts in this report.
```python
fig = plt.figure()
x = numpy.arange(len(unique_sectors))
width = 0.2
fig, ax = plt.subplots()
q4 = ax.bar(x - 1.5*width, [meds[sector][model.quarters[0]]
                            for sector in meds], width, label=model.quarters[0])
q1 = ax.bar(x - 0.5*width, [meds[sector][model.quarters[1]]
                            for sector in meds], width, label=model.quarters[1])
q2 = ax.bar(x + 0.5*width, [meds[sector][model.quarters[2]]
                            for sector in meds], width, label=model.quarters[2])
q3 = ax.bar(x + 1.5*width, [meds[sector][model.quarters[3]]
                            for sector in meds], width, label=model.quarters[3])
ax.axhline(color='black')
ax.set_ylabel('Median Debt Change / EBITDA')
ax.set_title('Median Debt Change / EBITDA by Sector, Last 4 Quarters')
ax.set_xticks(x)
ax.set_xticklabels(unique_sectors)
ax.legend()
```


### Sample Cumulative Line Chart Generation
The following is an example of the Python code that uses Matplotlib to generate a line chart showing the cumulative median debt change to normalized EBTIDA for each GICS sector for each quarter in study. Similar code was used for other line charts in this report.
```python
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(5), quarters)
for sector in unique_sectors:
    plt.plot(range(5), [0] + [sum(list(med_sector_dbt_ebd_cng[sector].values())[:(i+1)])
                              for i in range(len(model.quarters))],  label=sector)
plt.xlabel('Quarter')
ax.axhline(color='black')
plt.ylabel('Median Cumulative Debt Change/Normalized EBITDA')
plt.title('Median Cumulative Debt Change/Normalized EBITDA by Sector')
plt.tight_layout()
labelLines(plt.gca().get_lines())
```


## Appendix B: Setup
To run this project on your machine, first clone the repository:
```bash
git clone https://github.com/japplefield/fin342-corp-structure
```

Change into the cloned directory and create a virtual environment and install the required libraries:
```bash
cd fin342-corp-structure/
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Next, simply run the gen_graphs script:
```bash
./gen_graphs
```

To generate the database without generating graphs, run the file_import script:
```bash
./file_import.py
```
