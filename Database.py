import sqlite3

DB_NAME = "data/finance.db"


def connect():
    return sqlite3.connect(DB_NAME)


def initialize_database():

    conn = connect()

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        date TEXT,

        category TEXT,

        description TEXT,

        amount REAL,

        type TEXT
    )
    """)

    conn.commit()

    conn.close()
