import sqlite3

def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.
    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def sql_connection():
    try:
        con = sqlite3.connect('project.db')
        con.row_factory = dict_factory
        return con
    except sqlite3.Error:
        print(sqlite3.Error)

def strip_na(dct):
    return {key: dct[key] for key in dct if dct[key] != "#N/A"}
