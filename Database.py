import sqlite3
from datetime import datetime


DB_NAME = "data/finance.db"


def connect():

    return sqlite3.connect(DB_NAME)



def initialize_database():

    conn = connect()

    cur = conn.cursor()



    # ==========================
    # TRANSACTIONS TABLE
    # ==========================

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



    # ==========================
    # BUDGETS TABLE
    # ==========================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS budgets(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        category TEXT,

        amount REAL,

        month INTEGER,

        year INTEGER,

        UNIQUE(category, month, year)
    )
    """)



    # ==========================
    # INCOME FORECAST TABLE
    # ==========================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS income_forecast(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        source TEXT,

        expected_amount REAL,

        month INTEGER,

        year INTEGER,

        UNIQUE(source, month, year)
    )
    """)



    conn.commit()

    conn.close()





# ==========================
# TRANSACTIONS
# ==========================


def add_transaction(
        description,
        category,
        amount,
        transaction_type
):

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    INSERT INTO transactions
    (
        date,
        category,
        description,
        amount,
        type
    )

    VALUES
    (
        DATE('now'),
        ?,
        ?,
        ?,
        ?
    )
    """,
    (
        category,
        description,
        amount,
        transaction_type
    ))


    conn.commit()

    conn.close()





def get_transactions():

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    SELECT *

    FROM transactions

    ORDER BY id DESC
    """)


    transactions = cur.fetchall()


    conn.close()


    return transactions





def delete_transaction(transaction_id):

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    DELETE FROM transactions

    WHERE id = ?
    """,
    (
        transaction_id,
    ))


    conn.commit()

    conn.close()





# ==========================
# DASHBOARD FUNCTIONS
# ==========================


def get_monthly_income():

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    SELECT SUM(amount)

    FROM transactions

    WHERE type = 'Income'
    """)


    result = cur.fetchone()[0]


    conn.close()


    return result if result else 0





def get_monthly_expenses():

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    SELECT SUM(amount)

    FROM transactions

    WHERE type = 'Expense'
    """)


    result = cur.fetchone()[0]


    conn.close()


    return result if result else 0





def get_net_worth():

    return (
        get_monthly_income()
        -
        get_monthly_expenses()
    )





# ==========================
# BUDGET FUNCTIONS
# ==========================


def add_budget(
        category,
        amount,
        month=None,
        year=None
):

    if month is None:
        month = datetime.now().month


    if year is None:
        year = datetime.now().year



    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    INSERT INTO budgets
    (
        category,
        amount,
        month,
        year
    )

    VALUES
    (
        ?,
        ?,
        ?,
        ?
    )

    ON CONFLICT(category, month, year)

    DO UPDATE SET

        amount = excluded.amount

    """,
    (
        category,
        amount,
        month,
        year
    ))


    conn.commit()

    conn.close()





def get_budgets(
        month=None,
        year=None
):

    if month is None:
        month = datetime.now().month


    if year is None:
        year = datetime.now().year



    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    SELECT *

    FROM budgets

    WHERE month = ?

    AND year = ?

    ORDER BY category
    """,
    (
        month,
        year
    ))


    budgets = cur.fetchall()


    conn.close()


    return budgets





def update_budget(
        budget_id,
        category,
        amount
):

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    UPDATE budgets

    SET

        category = ?,

        amount = ?

    WHERE id = ?

    """,
    (
        category,
        amount,
        budget_id
    ))


    conn.commit()

    conn.close()





def delete_budget(
        budget_id
):

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    DELETE FROM budgets

    WHERE id = ?

    """,
    (
        budget_id,
    ))


    conn.commit()

    conn.close()





def get_category_spending(
        category,
        month=None,
        year=None
):

    if month is None:
        month = datetime.now().month


    if year is None:
        year = datetime.now().year



    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    SELECT SUM(amount)

    FROM transactions

    WHERE category = ?

    AND type = 'Expense'

    AND strftime('%m', date) = ?

    AND strftime('%Y', date) = ?

    """,
    (
        category,
        f"{month:02d}",
        str(year)
    ))


    result = cur.fetchone()[0]


    conn.close()


    return result if result else 0





# ==========================
# INCOME FORECAST FUNCTIONS
# ==========================


def add_income_forecast(
        source,
        expected_amount,
        month=None,
        year=None
):

    if month is None:
        month = datetime.now().month


    if year is None:
        year = datetime.now().year



    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    INSERT INTO income_forecast
    (
        source,
        expected_amount,
        month,
        year
    )

    VALUES
    (
        ?,
        ?,
        ?,
        ?
    )

    ON CONFLICT(source, month, year)

    DO UPDATE SET

        expected_amount = excluded.expected_amount

    """,
    (
        source,
        expected_amount,
        month,
        year
    ))


    conn.commit()

    conn.close()





def get_income_forecasts(
        month=None,
        year=None
):

    if month is None:
        month = datetime.now().month


    if year is None:
        year = datetime.now().year



    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    SELECT *

    FROM income_forecast

    WHERE month = ?

    AND year = ?

    ORDER BY source
    """,
    (
        month,
        year
    ))


    results = cur.fetchall()


    conn.close()


    return results





def get_actual_income(
        month=None,
        year=None
):

    if month is None:
        month = datetime.now().month


    if year is None:
        year = datetime.now().year



    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    SELECT SUM(amount)

    FROM transactions

    WHERE type = 'Income'

    AND strftime('%m', date) = ?

    AND strftime('%Y', date) = ?

    """,
    (
        f"{month:02d}",
        str(year)
    ))


    result = cur.fetchone()[0]


    conn.close()


    return result if result else 0





def get_income_variance(
        month=None,
        year=None
):

    forecasts = get_income_forecasts(
        month,
        year
    )


    expected = sum(
        item[2]
        for item in forecasts
    )


    actual = get_actual_income(
        month,
        year
    )


    return actual - expected