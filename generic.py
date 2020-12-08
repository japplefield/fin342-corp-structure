#!/usr/bin/env python3

import sys
sys.path.insert(1, 'handle_data/')
import statistics
import os
import model
import matplotlib.pyplot as plt
import numpy
from matplotlib import rcParams
from labellines import labelLine, labelLines

rcParams['figure.figsize'] = [12, 7]

con = model.sql_connection()
cur = con.cursor()

tables = ['eq_cng_shares_ebd_2', 'eq_cng_divs_ebd_2', 'eq_cng_tot_ebd_2', 'debt_cng_ebd']
table_labels = ['Equity Change from Share Issuance (Repurchase)/Normalized EBITDA', 'Equity Change from Dividends/Normalized EBITDA', 'Equity Change/Normalized EBITDA', 'Debt Change/Normalized EBITDA']
file_labels = ['eq_shares_cng_ebitda', 'eq_divs_cng_ebitda', 'eq_tot_cng_ebitda', 'debt_cng_ebd']

def gen_bar(dct, label, cat, file_label):
    try:
        os.mkdir(f'{cat} Bar Charts')
    except FileExistsError:
        pass
    x = numpy.arange(len(dct))
    width = 0.2
    fig, ax = plt.subplots()
    q4 = ax.bar(x - 1.5*width, [dct[comp][model.quarters[0]] for comp in dct], width, label=model.quarters[0])
    q1 = ax.bar(x - 0.5*width, [dct[comp][model.quarters[1]] for comp in dct], width, label=model.quarters[1])
    q2 = ax.bar(x + 0.5*width, [dct[comp][model.quarters[2]] for comp in dct], width, label=model.quarters[2])
    q3 = ax.bar(x + 1.5*width, [dct[comp][model.quarters[3]] for comp in dct], width, label=model.quarters[3])
    ax.axhline(color='black')
    ax.axhline(color='black')
    for i in range(len(dct) - 1):
        ax.axvline(x=0.5 + i, linestyle='dashed', color='green')
    ax.set_ylabel(f'{label}')
    ax.set_title(f'{label} for {cat}')
    ax.set_xticks(x)
    ax.set_xticklabels(dct.keys())
    fig.autofmt_xdate()
    ax.legend()
    plt.savefig(f'{cat} Bar Charts/{cat}_{file_label}.png',bbox_inches='tight')

def gen_line(dct, label, cat, file_label):
    try:
        os.mkdir(f'{cat} Cumulative Line Charts')
    except FileExistsError:
        pass
    quarters = ['Q32019'] + list(model.quarters)
    NUM_COLORS = len(dct)
    cm = plt.get_cmap('gist_rainbow')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    plt.xticks(numpy.arange(5), quarters)
    # plt.ylim(-0.4, 0.6)
    for comp in dct:
        plt.plot(range(5), [0] + [sum(list(dct[comp].values())[:(i+1)]) for i in range(len(model.quarters))],  label=comp)
    plt.xlabel('Quarter')
    ax.axhline(color='black')
    plt.ylabel(f'Cumulative {label}')
    plt.title(f'Cumulative {label} for {cat}')
    # plt.tight_layout()
    try:
        labelLines(plt.gca().get_lines())
    except:
        pass
    plt.savefig(f'{cat} Cumulative Line Charts/{cat}_{file_label}_cum.png',bbox_inches='tight')

def gen_graphs(gics_type, cat):
    for i in range(len(tables)):
        cur.execute(f"SELECT * FROM {tables[i]} INNER JOIN gics ON {tables[i]}.symbol=gics.symbol WHERE gics.{gics_type}='{cat}'")
        rows = cur.fetchall()
        res = {row['symbol']: {quarter: row[quarter] for quarter in model.quarters} for row in rows}
        dct = {comp: res[comp] for comp in res if None not in res[comp].values()}
        gen_bar(dct, table_labels[i], cat, file_labels[i])
        gen_line(dct, table_labels[i], cat, file_labels[i])

        # Close Database
        con.commit()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print ("Usage: generic.py <gics type> <gics classification>")
        exit(1)
    gen_graphs(sys.argv[1], sys.argv[2])
