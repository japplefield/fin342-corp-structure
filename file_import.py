#!/usr/bin/env python
import model
import read_meta, read_debt, read_equity
from sqlite3 import OperationalError as DBError

def read_files(cur):
    try:
        read_meta.read_gics(cur)
    except DBError:
        pass
    try:
        read_meta.read_ebitda(cur)
    except DBError as e:
        print(e.args[0])
    try:
        read_debt.read_debt(cur)
    except DBError as e:
        print(e.args[0])
    try:
        read_debt.cng_dbt_ebd(cur)
    except DBError as e:
        print(e.args[0])
    try:
        read_equity.read_prices(cur)
    except DBError as e:
        print(e.args[0])
    try:
        read_equity.read_shares(cur)
    except DBError as e:
        print(e.args[0])
    try:
        read_equity.read_dividends(cur)
    except DBError as e:
        print(e.args[0])
    try:
        read_equity.calc_eq_cng(cur)
    except DBError as e:
        print(e.args[0])
    try:
        read_equity.calc_eq_cng_ebd(cur)
    except DBError as e:
        print(e.args[0])
    try:
        read_equity.eq_cng_ebd_refactor(cur)
    except DBError as e:
        print(e.args[0])

if __name__ == '__main__':
    con = model.sql_connection()
    cur = con.cursor()

    read_files(cur)

    # Close Database
    con.commit()
