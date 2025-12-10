import sqlite3

# Created to avoid circular imports

# configure database, rows will behave like dictionaries
def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect('bomanis_vault.db')
    conn.row_factory = sqlite3.Row
    return conn