./handle_data/file_import.py

mkdir 'Debt Bar Charts'
mkdir 'Debt Cumulative Line Charts'
mkdir 'Equity Bar Charts'
mkdir 'Equity Cumulative Line Charts'

for FILE in $(ls summary_graphs/ | egrep '*.py')
do
    ./summary_graphs/$FILE
done
