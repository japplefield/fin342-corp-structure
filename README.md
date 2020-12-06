# FIN 342 Project: Tracking Corporate Structure Changes due to COVID-19

## Table of Contents
* [Introduction](#introduction)
* [Data](#data)
* [Technologies](#technologies)
* [Methodology](#methodology)
* [Setup](#setup)

## Introduction
In early 2020, markets took a huge dive as the COVID-19 pandemic worsened. Uncertainty has led to lots of cost cutting, but what will the actual effect be on corporations’ ability to pay off their debt? On the other hand, low interest rates might lead companies to try to acquire more debt for cheap. What is the net effect these two conflicting trends might have on corporate structure and debt levels, and how does this vary by industry? An analysis will help understand a lot about how each industry is affected by things like consumer trends and the Fed’s policies, and may provide some future insight about what industries may be exposed to higher leverage risk going forward.

## Data
The data set will comprise of S&P 1500 companies’ balance sheets and debt schedules pre-COVID-19 and currently. Data includes:
* Debt during each of the past five quarters and EBITDA on an historical, annual basis over a few years ending December 2019.
* Dividends per share over the past four Quarters
* Share price every day the past four Quarters
* Shares outstanding quarterly the past five Quarters
* GICS classification meta-data

## Methodology
I will compute a normalized EBITDA using the past few years EBITDA for each company. can compute Debt/normalized EBITDA for each company at December 31, 2019, March 31, 2020, June 30, 2020 and September 30, 2020. Then, I will compute industry median Debt/normalized EBITDA over these 4 estimation dates to describe how industry leverage has changed over the COVID-19 window. Next, I will compute an average share price for each company for each quarter in study, and determine the total equity value raised or returned to shareholders as a result of:
* Share issuance or buybacks (assuming these all occurred at the average share price that quarter)
* Dividend payment

An extension to this analysis would be to determine whether there is a relationship between corporate bond yields and leverage changes (for example, does the data show reductions in leverage during quarters when corporate bond yields increased, and increases in leverage during quarters when corporate bond yields decreased; and if industry corporate bond yields are available, are changes in corporate bond yields by industry associated with changes in leverage by industry).

## Setup
To run this project on your machine, first clone the repository:
```bash
git clone https://github.com/japplefield/fin342-corp-structure
```

Create a virtual environment and install the required libraries:
```bash
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
