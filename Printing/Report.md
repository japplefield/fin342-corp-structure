---
title: Pandemic Induced Restructuring
author: Justin Applefield (jmapple)
date: \today
papersize: letter
fontsize: 11pt
geometry:
- margin=1in
linkcolor: blue
header-includes: |
    \usepackage{multicol}
    \usepackage{wrapfig}
---

## Table of Contents
* [Introduction](#introduction)
* [Data](#data)
* [Technologies](#technologies)
* [Methodology](#methodology)
* [Results](#results)
    * [Quarterly Change in Debt and Equity](#quarterly-change-in-debt-and-equity)
    * [Cumulative Change in Debt and Equity](#cumulative-change-in-debt-and-equity)
    * [Industries of Particular Interest](#industries-of-particular-interest)
* [Conclusion](#conclusion)
* [Appendices](#appendix-a-summary-tables)
    * [Appendix A: Summary Tables](#appendix-a-summary-tables)
    * [Appendix B: Sample Code](#appendix-b-sample-code)
    * [Appendix C: Setup](#appendix-c-setup)

## Introduction
In early 2020, markets took a huge dive as the COVID-19 pandemic worsened. Uncertainty has led to lots of cost cutting, and some companies could _still_ be scrambling for cash. Might this inhibit corporations' abilities to pay off their debt? On the other hand, low interest rates might lead companies to try to acquire more debt for cheap. What is the net effect these two conflicting trends might have on corporate structure and debt levels, and how does this vary by industry? And with the lower cost of borrowing, will firms overwhelmingly prefer to borrow to raise capital, rather than issue shares? An analysis will help understand a lot about how each industry is affected by things like consumer trends and the Fed’s policies, and provide insight about what industries are exposed to higher leverage risk going forward. It also provides insight into how much financial strain companies are feeling as a result of the pandemic.

## Data
The data set comprises of S&P 1500 companies’ balance sheets and debt schedules pre-COVID-19 and currently. The S&P 1500 was chosen because it covers approximately 90% of the total market capitalization of US stocks,[^1] and is therefore representative of the US market as a whole. Data was retrieved from FactSet. The firm-by-firm data include:

[^1]: https://www.spglobal.com/spdji/en/indices/equity/sp-composite-1500/#overview

* Debt during each of the past five quarters and EBITDA on an historical, annual basis over a few years ending December 2019 for all available firms
* Quarterly dividends per share from Q4 2019 to Q3 2020 for all available firms
* Share price every day from October 1, 2019 to September 30, 2020 for all available firms
* Quarterly shares outstanding from Q4 2019 to Q3 2020 for all available firms
* GICS classification meta-data for all S&P 1500 companies

Because only data where all this information was available for a given firm was usable, the final data set included only 1322 firms. The majority of these excluded firms are banks/financial services companies where EBITDA information was not available, as EBITDA does not have the same relevance for financials firms as it does for industrial firms.

## Methodology
I computed a normalized EBITDA as the mean of the 2015-2019 annual EBITDAs for each company. I then computed change in total debt each quarter. Next, to represent change in equity value, I calculated an average share price for each company for each quarter in study, and determined the total equity value raised or returned to shareholders as a result of:

* Share issuance or buybacks (assuming these all occurred at the average share price that quarter)
* Dividend payment

Equity value from share issuance or buybacks was calculated as:
$$
\Delta \text{Eq} = \text{Quarterly Avg Price} \times \Delta \text{Shares Outstanding}
$$
The result from the above equation is positive for share issuance and negative for share repurchase.
Equity value from dividend payments was calculated as:
$$
\Delta \text{Eq} = -1 \times \text{Dividends per Share} \times \text{Shares Outstanding}
$$
The result from the above equation is always negative.

I then computed the following ratios for each company on December 31, 2019, March 31, 2020, June 30, 2020 and September 30, 2020:

* Change in Total Debt/normalized EBITDA
* Change in Equity Value/normalized EBITDA
* Change in Equity Value attributable to dividend payments/normalized EBITDA
* Change in Equity Value attributable to share issuance or repurchase/normalized EBITDA
* Change in Total Debt + Equity/normalized EBITDA

## Technologies
Python was used to handle all data management and graph generation. The relational database management system used was SQLite, as it is included in the Python Standard Library. For graph generation, Matplotlib and NumPy were used. [Github user cphyc's project matplotlib-label-lines](https://github.com/cphyc/matplotlib-label-lines) was also used to make some of the graphs more readable.

Sample SQL and Python code can be found in [Appendix B](#appendix-b-sample-code).

## Results
### Quarterly Change in Debt and Equity
After calculating the above four ratios for all 1322 companies with complete data, I calculated medians for each of the 11 GICS Sectors for each of the past four quarters. These medians are graphed below:

\begin{figure}[!h]
\caption{The median ratios for each of the 11 GICS Sectors Q4 2019 to Q3 2020}
\end{figure}
![](../Debt_Bar_Charts/med_debt_cng_ebitda_all.png){ width=50% }
![](../Equity_Bar_Charts/med_eq_divs_cng_ebitda_all.png){ width=50% }
![](../Equity_Bar_Charts/med_eq_shares_cng_ebitda_all.png){ width=50% }
![](../Equity_Bar_Charts/med_eq_tot_cng_ebitda_all.png){ width=50% }
\begin{wrapfigure}{l}{0.5\linewidth}
\includegraphics[width=\linewidth]{../Total_Bar_Charts/med_tot_eq_debt_cng_ebitda_all.png}
\end{wrapfigure}
Some notable conclusions can be drawn from the above graphs. First, a lot of firms continued to pay dividends despite the financial strain on the economy as a whole. The median real estate firm paid out approximately 0.13x its annual EBITDA as a dividend at the end of each of the studied quarters. Part of this is attributable to SEC requirements that real estate investment trusts (REITs) must pay out 90\% of their taxable income annually in the form of dividends.[^2] The amount of equity raised from share issuance trended upwards over the past four quarters. Sectors like information technology and health care both saw sharp increases in equity raised by share issuance in Q3 2020. Perhaps the most important takeaway from the above graphs is that the magnitude of capital raised by issuing debt, on average, far exceeded that of capital raised by issuing equity. The median consumer discretionary and real estate firm both issued debt on the order of 0.4-0.5x their annual EBITDA during just Q1 2020. While this could be a sign of financial distress due to COVID, it could also be a result of the incredibly low cost of borrowing.

[^2]: https://www.sec.gov/files/reits.pdf

### Cumulative Change in Debt and Equity
Next, I graphed the running sum of each of the four ratios to quantify cumulative effect of changes in debt and equity across the past four quarters, holding levels at the end of Q3 2019 as the "0." The graphs are below.

\begin{figure}[!h]
\caption{The median cumulative sum of the four ratios for each of the 11 GICS Sectors}
\end{figure}
![](../Debt_Cumulative_Line_Charts/med_debt_cng_ebitda_cum_all.png){ width=50% }
![](../Equity_Cumulative_Line_Charts/med_eq_divs_cng_ebitda_cum_all.png){ width=50% }
![](../Equity_Cumulative_Line_Charts/med_eq_shares_cng_ebitda_cum_all.png){ width=50% }
![](../Equity_Cumulative_Line_Charts/med_eq_tot_cng_ebitda_cum_all.png){ width=50% }
\begin{wrapfigure}{l}{0.5\linewidth}
\includegraphics[width=\linewidth]{../Total_Cumulative_Line_Charts/med_tot_eq_debt_cng_ebitda_cum_all.png}
\end{wrapfigure}
One key takeaway from the above charts is that although some firms are issuing a substantial amount of shares, on average the decrease in total equity attributable to dividends is much larger quarter over quarter, to the extent that firms have much less equity financed now than they did a year ago. On the debt side, in many sectors firms took on a lot of debt at the start of 2020 and have since reduced their debt amounts by quite a bit. The net result of these two effects is that the median firm today has cumulatively paid out approximately as much in dividends as it has taken on in debt over the past year.

### Industries of Particular Interest
The COVID-19 pandemic has had a profound impact on consumer habits. Particularly, travel for both business and leisure has decreased substantially as it was perceived as unsafe and other countries imposed entry restrictions, and e-commerce has grown as consumers have feared going to brick-and-mortar stores. Therefore, I decided it would be interesting to look specifically and the change in debt and equity for firms in the Airlines, Hotels Resorts & Cruise Lines, and Internet & Direct Marketing Retail GICS Sub-Industries.

\begin{figure}[!h]
\caption{Cumulative change in debt and equity for Airlines}
\end{figure}
![](../Airlines_Cumulative_Line_Charts/Airlines_debt_cng_ebd_cum.png){ width=50% }
![](../Airlines_Cumulative_Line_Charts/Airlines_eq_tot_cng_ebitda_cum.png){ width=50% }
\begin{wrapfigure}{l}{0.5\linewidth}
\includegraphics[width=\linewidth]{../Airlines_Cumulative_Line_Charts/Airlines_tot_eq_debt_cng_ebitda_cum.png}
\end{wrapfigure}
The above charts show the cumulative change in debt and equity for Airlines over the past year. While some airlines have seen a cumulative decrease in equity (largely due to payment of dividends) over the past year on the order of 0.1x annual EBITDA, some (Southwest, United, and American) have issued shares, and nearly all have taken on debt, with some (JetBlue and Delta) taking on debt in excess of 2.0x annual EBITDA over the past year. I interpret this to be a sign of financial distress for the airline industry, as they are turning to all possible avenues to raise capital rather than just re-levering. This idea is supported by the notion that, with business and leisure air travel and recent lows, airlines would feel severe amounts of financial stress.

\newpage

\begin{figure}[!h]
\caption{Cumulative change in debt and equity for Hotels Resorts \& Cruise Lines}
\end{figure}
![](../Hotels_Resorts___Cruise_Lines_Cumulative_Line_Charts/Hotels_Resorts___Cruise_Lines_debt_cng_ebd_cum.png){ width=50% }
![](../Hotels_Resorts___Cruise_Lines_Cumulative_Line_Charts/Hotels_Resorts___Cruise_Lines_eq_tot_cng_ebitda_cum.png){ width=50% }
\begin{wrapfigure}{l}{0.5\linewidth}
\includegraphics[width=\linewidth]{../Hotels_Resorts___Cruise_Lines_Cumulative_Line_Charts/Hotels_Resorts___Cruise_Lines_tot_eq_debt_cng_ebitda_cum.png}
\end{wrapfigure}
The above charts show the cumulative change in debt and equity for hotels, resorts, and cruise lines over the past year. Dividends were paid by many firms in Q4 2019 and Q1 2020 but these firms did not make payments in Q2 and Q3 2020. There was also lots of debt accumulation in Q1 2020, likely due to the lower cost of borrowing. While some companies in this sub-industry kept debt level for the past two quarters, cruise lines took on even more debt in Q2 and Q3, while some companies were able to pay a little off like Marriott and Choice Hotels. The reduction in debt for hotel chains could be attributable to just maturing obligations, or could be due to the fact that of all the travel related categories, hotels are able to best cope with reduced demand because they can take advantage of trends like increases in road tripping and domestic travel, can cope with decreased business travel, and can maintain a standard of cleanliness better than airlines or cruise lines. Some firms, like the cruise lines, did issue shares in addition to taking on more debt, possibly because it is hard to get good rates on all offered debt due to intrinsic business risk. Eventually it becomes cheaper to issue more shares than to take on debt. For all firms in this sub-industry, the increase in debt is much larger than the decrease in equity from dividend payments.

\newpage

\begin{figure}[!h]
\caption{Cumulative change in debt and equity for Internet \& Direct Marketing Retail}
\end{figure}
![](../Internet___Direct_Marketing_Retail_Cumulative_Line_Charts/Internet___Direct_Marketing_Retail_debt_cng_ebd_cum.png){ width=50% }
![](../Internet___Direct_Marketing_Retail_Cumulative_Line_Charts/Internet___Direct_Marketing_Retail_eq_tot_cng_ebitda_cum.png){ width=50% }
\begin{wrapfigure}{l}{0.5\linewidth}
\includegraphics[width=\linewidth]{../Internet___Direct_Marketing_Retail_Cumulative_Line_Charts/Internet___Direct_Marketing_Retail_tot_eq_debt_cng_ebitda_cum.png}
\end{wrapfigure}
The above charts show the cumulative change in debt and equity for internet & direct marketing retail. Based on the charts, the typical internet & direct marketing retail firm did not need to take on much debt, but companies that rely on travel (like Expedia) did. Some companies issued an observable amount of shares. Amazon, for example, issued a small amount of shares in addition to issuing debt because their share price is so high that they can get a lot of value for issuing shares without diluting their equity by much. This registers as a large increase in equity despite being a small quantity of shares because of their high share price. Meanwhile, eBay bought back shares in Q1 2020 before the pandemic hit coinciding with its sale of Stubhub.[^3] It makes sense that eBay has not further changed its capital structure since the share repurchase, as it is a firm that would be expected to maintain stability during the pandemic; as more people have free time and need extra cash they might turn to eBay to make extra cash, as well as benefiting from an increase in consumer goods spending. The typical firm in this sub-industry did not change its capital structure much, probably because this is a stable sub-industry that benefited marginally from COVID but ultimately received little impact.

[^3]: https://www.reuters.com/article/us-ebay-outlook/ebay-raises-share-buyback-plan-forecasts-strong-first-quarter-profit-idUSKBN2072XS

## Conclusion

The data support the idea that firms would take advantage of low interest rates and take on more debt while continuing to pay out dividends. On the scale of the whole market, this seems to be what happened, which could be interpreted as a signal that the average firm has financially not reacted much to any direct effects of the pandemic, and instead has reacted to governmental intervention like the lowering of rates that came at the same time the pandemic hit. Sub-industries that are directly and negatively affected by changing consumer behavior due to the pandemic, such as airlines, hotels, resorts, and cruise lines, have both taken on debt and issued shares. This supports the notion that if rates are low, firms would take on as much debt as they can until it is cheaper to take on equity, and then if they still need more cash to obtain it through issuing shares. This excess need for cash could be interpreted as a signal that these firms are in a state of financial distress, as they needed cash but were not able to get sufficient cash at efficient interest rates and/or feel unconfident in their future ability to pay off debt. Therefore, I believe there is a positive association between share issuance and financial distress during the COVID-19 pandemic.

\newpage

## Appendix A: Summary Tables

Table 1: Median change in Total Debt/normalized EBITDA by GICS sector

| Sector                 |  Q4 2019 |  Q1 2020 |  Q2 2020 |  Q3 2020 |
|------------------------|---------:|---------:|---------:|---------:|
| Information Technology | 0.002   | 0.004   | (0.005) | (0.009) |
| Industrials            | (0.011) | 0.166   | (0.058) | (0.035) |
| Health Care            | (0.001) | 0.041   | (0.004) | (0.021) |
| Consumer Discretionary | (0.008) | 0.490   | (0.041) | (0.066) |
| Real Estate            | 0.049   | 0.443   | (0.063) | (0.001) |
| Communication Services | (0.007) | (0.013) | 0.000   | (0.001) |
| Materials              | (0.017) | 0.195   | (0.045) | (0.105) |
| Financials             | 0.009   | 0.125   | (0.078) | 0.011   |
| Utilities              | 0.108   | 0.188   | 0.059   | 0.066   |
| Consumer Staples       | (0.001) | 0.182   | (0.094) | (0.013) |
| Energy                 | (0.005) | (0.005) | (0.002) | (0.007) |
| **All**                    | **(0.001)** | **0.120**   | **(0.016)** | **(0.014)** |

Table 2: Median change in Equity Value/normalized EBITDA by GICS sector

| Sector                 |  Q4 2019 |  Q1 2020 |  Q2 2020 |  Q3 2020 |
|------------------------|---------:|---------:|---------:|---------:|
| Information Technology | (0.032) | (0.017) | (0.037) | 0.010   |
| Industrials            | (0.036) | (0.035) | (0.038) | (0.015) |
| Health Care            | 0.001   | 0.003   | 0.000   | 0.007   |
| Consumer Discretionary | (0.048) | (0.042) | 0.000   | 0.002   |
| Real Estate            | (0.095) | (0.097) | (0.098) | (0.083) |
| Communication Services | (0.023) | (0.016) | (0.018) | 0.000   |
| Materials              | (0.046) | (0.033) | (0.043) | (0.030) |
| Financials             | (0.083) | (0.039) | (0.046) | (0.045) |
| Utilities              | (0.050) | (0.039) | (0.059) | (0.056) |
| Consumer Staples       | (0.058) | (0.059) | (0.059) | (0.048) |
| Energy                 | (0.034) | (0.019) | (0.001) | 0.000   |
| **All**                    | **(0.043)** | **(0.032)** | **(0.033)** | **(0.006)** |

\newpage

Table 3: Median change in Equity Value attributable to dividend payments/normalized EBITDA by GICS sector

| Sector                 |  Q4 2019 |  Q1 2020 |  Q2 2020 |  Q3 2020 |
|------------------------|---------:|---------:|---------:|---------:|
| Information Technology | 0.000   | 0.000   | 0.000   | 0.000   |
| Industrials            | (0.026) | (0.025) | (0.024) | (0.022) |
| Health Care            | 0.000   | 0.000   | 0.000   | 0.000   |
| Consumer Discretionary | (0.022) | (0.017) | 0.000   | 0.000   |
| Real Estate            | (0.147) | (0.139) | (0.123) | (0.126) |
| Communication Services | (0.018) | 0.000   | 0.000   | 0.000   |
| Materials              | (0.042) | (0.040) | (0.041) | (0.040) |
| Financials             | (0.049) | (0.048) | (0.047) | (0.047) |
| Utilities              | (0.063) | (0.061) | (0.065) | (0.065) |
| Consumer Staples       | (0.052) | (0.053) | (0.051) | (0.043) |
| Energy                 | (0.017) | (0.006) | 0.000   | 0.000   |
| **All**                    | **(0.030)** | **(0.025)** | **(0.015)** | **(0.012)** |

Table 4: Median change in Equity Value attributable to share issuance (repurchase)/normalized EBITDA by GICS sector

| Sector                 |  Q4 2019 |  Q1 2020 |  Q2 2020 |  Q3 2020 |
|------------------------|---------:|---------:|---------:|---------:|
| Information Technology | 0.001   | 0.012   | 0.000   | 0.032  |
| Industrials            | 0.000   | 0.003   | 0.000   | 0.005  |
| Health Care            | 0.004   | 0.005   | 0.006   | 0.024  |
| Consumer Discretionary | 0.000   | (0.001) | 0.002   | 0.005  |
| Real Estate            | 0.007   | 0.013   | 0.003   | 0.004  |
| Communication Services | 0.001   | 0.002   | 0.003   | 0.005  |
| Materials              | 0.000   | 0.002   | 0.000   | 0.002  |
| Financials             | (0.006) | 0.002   | (0.002) | 0.002  |
| Utilities              | 0.004   | 0.012   | 0.006   | 0.004  |
| Consumer Staples       | 0.001   | 0.003   | 0.000   | 0.003  |
| Energy                 | 0.000   | 0.004   | 0.000   | 0.002  |
| **All**                    | **0.000**   | **0.004**   | **0.001**   | **0.006**  |

\newpage

Table 5: Median change in Total Debt + Equity Value/normalized EBITDA by GICS sector

| Sector                 |  Q4 2019 |  Q1 2020 |  Q2 2020 |  Q3 2020 |
|------------------------|---------:|---------:|---------:|---------:|
| Information Technology | (0.044) | 0.036   | (0.112) | (0.024) |
| Industrials            | (0.069) | 0.103   | (0.148) | (0.076) |
| Health Care            | (0.009) | 0.064   | (0.010) | (0.025) |
| Consumer Discretionary | (0.077) | 0.443   | (0.098) | (0.087) |
| Real Estate            | (0.041) | 0.520   | (0.170) | (0.063) |
| Communication Services | (0.057) | (0.059) | (0.002) | 0.003   |
| Materials              | (0.096) | 0.128   | (0.088) | (0.136) |
| Financials             | (0.110) | 0.068   | (0.138) | (0.025) |
| Utilities              | 0.070   | 0.148   | 0.024   | 0.019   |
| Consumer Staples       | (0.093) | 0.104   | (0.208) | (0.094) |
| Energy                 | (0.087) | (0.044) | (0.024) | (0.037) |
| **All**                    | **(0.054)** | **0.112**   | **(0.092)** | **(0.049)** |

\newpage

## Appendix B: Sample Code

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

\newpage

### Sample Bar Chart Generation
The following is an example of the Python code that uses Matplotlib to generate a bar chart showing the median debt change to normalized EBTIDA for each GICS sector for each quarter in study. Similar code was used for other bar charts in this report.
```python
x = numpy.arange(len(dct))
width = 0.2
fig, ax = plt.subplots()
q4 = ax.bar(x - 1.5*width, [dct[comp][model.quarters[0]]
                            for comp in dct], width, label=model.quarters[0])
q1 = ax.bar(x - 0.5*width, [dct[comp][model.quarters[1]]
                            for comp in dct], width, label=model.quarters[1])
q2 = ax.bar(x + 0.5*width, [dct[comp][model.quarters[2]]
                            for comp in dct], width, label=model.quarters[2])
q3 = ax.bar(x + 1.5*width, [dct[comp][model.quarters[3]]
                            for comp in dct], width, label=model.quarters[3])
ax.axhline(color='black')
for i in range(len(dct) - 1):
    ax.axvline(x=0.5 + i, linestyle='dashed', color='green')
ax.set_ylabel(f'{label}')
ax.set_title(f'{label} for {cat}')
ax.set_xticks(x)
ax.set_xticklabels(dct.keys())
fig.autofmt_xdate()
ax.legend()
```

### Sample Cumulative Line Chart Generation
The following is an example of the Python code that uses Matplotlib to generate a line chart showing the cumulative median debt change to normalized EBTIDA for each GICS sector for each quarter in study. Similar code was used for other line charts in this report.
```python
quarters = ['Q32019'] + list(model.quarters)
NUM_COLORS = len(dct)
cm = plt.get_cmap('gist_rainbow')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
plt.xticks(numpy.arange(5), quarters)
for comp in dct:
    plt.plot(range(5), [0] + [sum(list(dct[comp].values())[:(i+1)])
                              for i in range(len(model.quarters))],  label=comp)
plt.xlabel('Quarter')
ax.axhline(color='black')
plt.ylabel(f'Cumulative {label}')
plt.title(f'Cumulative {label} for {cat}')
```

\newpage

## Appendix C: Setup
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
./gen_graphs.sh
```

To generate the database without generating graphs, run the file_import script:
```bash
./file_import.py
```

To generate graphs for any GICS grouping, you can run the generic script as follows:
```bash
./generic.py <gics type> <gics classification>
```
It is strongly recommended to only use this for GICS Industries or Sub Industries. Trying to use this script for GICS Sectors or Industry Groups will result in graphs with too many companies that are difficult to interpret. GICS type should be entered as a single word joined by underscores (i.e. Sector, Industry_Group, Industry, and Sub_Industry), while GICS classification should be entered as a quoted string with no commas (e.g. 'Hotels Resorts & Cruise Lines')
