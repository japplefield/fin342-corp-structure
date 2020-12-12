#!/bin/bash

./handle_data/file_import.py

mkdir 'Debt_Bar_Charts'
mkdir 'Debt_Cumulative_Line_Charts'
mkdir 'Equity_Bar_Charts'
mkdir 'Equity_Cumulative_Line_Charts'
mkdir 'Total_Bar_Charts'
mkdir 'Total_Cumulative_Line_Charts'

for FILE in $(ls summary_graphs/ | egrep '*.py')
do
    ./summary_graphs/$FILE
done
