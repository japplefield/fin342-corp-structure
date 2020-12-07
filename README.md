# FIN 342 Project: Pandemic Induced Restructuring

## Table of Contents
* [Introduction](#introduction)
* [Data](#data)
* [Technologies](#technologies)
* [Methodology](#methodology)
* [Setup](#setup)

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

Below is a summary of specific syntaxes used to read, manage, and display data:

### Sample Database Schema
The following is an example of the database schema used to store final ratios used.
```SQL
CREATE TABLE debt_cng_ebd symbol text UNIQUE,
             q42019 float DEFAULT NULL,
             q12020 float DEFAULT NULL,
             q22020 float DEFAULT NULL,
             q32020 float DEFAULT NULL);
```
A similar structure was used for the equity final summary tables: eq_cng_tot_ebd_2, eq_cng_shares_ebd_2, and eq_cng_divs_ebd_2

### Sample Database Query for Sector Summary Charts

### Sample Bar Chart Generation Code

### Sample Cumulative Line Chart Generation Code

## Setup
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
