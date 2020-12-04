import sqlite3

def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.
    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def sql_connection():
    try:
        con = sqlite3.connect('database.db')
        con.row_factory = dict_factory
        return con
    except sqlite3.Error:
        print(sqlite3.Error)

def sql_table(con):
    cur = con.cursor()
    # cur.execute("CREATE TABLE employees("
    #             "id integer PRIMARY KEY, "
    #             "name text, "
    #             "salary real, "
    #             "department text, "
    #             "position text, "
    #             "hireDate text)"
    #             )
    # cur.execute("INSERT INTO employees VALUES(1, 'John', 700, 'HR', 'Manager', '2017-01-04')")
    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    con.commit()
con = sql_connection()
sql_table(con)
