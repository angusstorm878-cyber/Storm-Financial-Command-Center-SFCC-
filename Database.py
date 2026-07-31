import sqlite3
from datetime import datetime

from migrations import run_migrations


DB_NAME = "data/finance.db"


def connect():

    conn = sqlite3.connect(DB_NAME)

    run_migrations(
        conn
    )

    return conn



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

# ==========================
# RECURRING TRANSACTIONS TABLE
# ==========================

    cur.execute("""
CREATE TABLE IF NOT EXISTS recurring_transactions(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    description TEXT,

    category TEXT,

    amount REAL,

    type TEXT,

    frequency TEXT,

    next_date TEXT,

    active INTEGER DEFAULT 1
)
""")



# ==========================
# RECEIPTS TABLE
# ==========================

    cur.execute("""
CREATE TABLE IF NOT EXISTS receipts(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    transaction_id INTEGER,

    vendor TEXT,

    amount REAL,

    date TEXT,

    file_path TEXT,

    notes TEXT,

    FOREIGN KEY(transaction_id)
    REFERENCES transactions(id)

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





def get_income_forecast_by_id(
        income_id
):

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    SELECT *

    FROM income_forecast

    WHERE id = ?

    """,
    (
        income_id,
    ))


    result = cur.fetchone()


    conn.close()


    return result





def update_income_forecast(
        income_id,
        source,
        expected_amount
):

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    UPDATE income_forecast

    SET

        source = ?,

        expected_amount = ?

    WHERE id = ?

    """,
    (
        source,
        expected_amount,
        income_id
    ))


    conn.commit()

    conn.close()





def delete_income_forecast(
        income_id
):

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    DELETE FROM income_forecast

    WHERE id = ?

    """,
    (
        income_id,
    ))


    conn.commit()

    conn.close()





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
# ==========================
# RECURRING TRANSACTION FUNCTIONS
# ==========================


def add_recurring_transaction(
        description,
        category,
        amount,
        transaction_type,
        frequency,
        next_date
):

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    INSERT INTO recurring_transactions
    (
        description,
        category,
        amount,
        type,
        frequency,
        next_date
    )

    VALUES
    (
        ?,
        ?,
        ?,
        ?,
        ?,
        ?
    )
    """,
    (
        description,
        category,
        amount,
        transaction_type,
        frequency,
        next_date
    ))


    conn.commit()

    conn.close()




def get_recurring_transactions():

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    SELECT *

    FROM recurring_transactions

    ORDER BY next_date
    """)


    results = cur.fetchall()


    conn.close()


    return results




def get_recurring_transaction_by_id(
        recurring_id
):

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    SELECT *

    FROM recurring_transactions

    WHERE id = ?
    """,
    (
        recurring_id,
    ))


    result = cur.fetchone()


    conn.close()


    return result




def update_recurring_transaction(
        recurring_id,
        description,
        category,
        amount,
        transaction_type,
        frequency,
        next_date
):

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    UPDATE recurring_transactions

    SET

        description = ?,

        category = ?,

        amount = ?,

        type = ?,

        frequency = ?,

        next_date = ?

    WHERE id = ?

    """,
    (
        description,
        category,
        amount,
        transaction_type,
        frequency,
        next_date,
        recurring_id
    ))


    conn.commit()

    conn.close()




def delete_recurring_transaction(
        recurring_id
):

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    DELETE FROM recurring_transactions

    WHERE id = ?
    """,
    (
        recurring_id,
    ))


    conn.commit()

    conn.close()

    # ==========================
# RECURRING AUTOMATION FUNCTIONS
# ==========================


def get_due_recurring_transactions():

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    SELECT *

    FROM recurring_transactions

    WHERE active = 1

    AND next_date <= DATE('now')
    """)


    results = cur.fetchall()


    conn.close()


    return results




def create_transaction_from_recurring(
        recurring_transaction
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
        recurring_transaction[2],
        recurring_transaction[1],
        recurring_transaction[3],
        recurring_transaction[4]
    ))


    conn.commit()

    conn.close()




def update_recurring_next_date(
        recurring_id,
        frequency
):

    conn = connect()

    cur = conn.cursor()


    if frequency == "Weekly":

        interval = "+7 days"


    elif frequency == "Biweekly":

        interval = "+14 days"


    elif frequency == "Monthly":

        interval = "+1 month"


    elif frequency == "Yearly":

        interval = "+1 year"


    else:

        interval = "+1 month"



    cur.execute("""
    UPDATE recurring_transactions

    SET next_date = DATE(next_date, ?)

    WHERE id = ?

    """,
    (
        interval,
        recurring_id
    ))


    conn.commit()

    conn.close()

    # ==========================
# PROCESS RECURRING TRANSACTIONS
# ==========================


def process_recurring_transactions():

    due_transactions = get_due_recurring_transactions()


    processed = 0


    for recurring in due_transactions:


        create_transaction_from_recurring(
            recurring
        )


        update_recurring_next_date(
            recurring[0],
            recurring[5]
        )


        processed += 1



    return processed

# ==========================
# DASHBOARD INTELLIGENCE FUNCTIONS
# ==========================


def get_monthly_summary(
        month=None,
        year=None
):

    if month is None:
        month = datetime.now().month


    if year is None:
        year = datetime.now().year



    income = get_actual_income(
        month,
        year
    )


    expenses = 0


    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    SELECT SUM(amount)

    FROM transactions

    WHERE type = 'Expense'

    AND strftime('%m', date) = ?

    AND strftime('%Y', date) = ?

    """,
    (
        f"{month:02d}",
        str(year)
    ))


    result = cur.fetchone()[0]


    if result:

        expenses = result


    conn.close()



    return {
        "income": income,
        "expenses": expenses,
        "net": income - expenses
    }





def get_upcoming_recurring_transactions():

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    SELECT *

    FROM recurring_transactions

    WHERE active = 1

    ORDER BY next_date

    LIMIT 5

    """)


    results = cur.fetchall()


    conn.close()


    return results





def get_budget_health():

    budgets = get_budgets()


    results = []


    for budget in budgets:

        category = budget[1]

        limit = budget[2]


        spent = get_category_spending(
            category
        )


        remaining = limit - spent


        if limit > 0:

            percentage = (
                spent / limit
            ) * 100

        else:

            percentage = 0



        results.append(
            {
                "category": category,
                "limit": limit,
                "spent": spent,
                "remaining": remaining,
                "percentage": percentage
            }
        )


    return results





def get_cash_flow_projection():

    summary = get_monthly_summary()


    recurring = get_upcoming_recurring_transactions()


    projected_income = summary["income"]

    projected_expenses = summary["expenses"]


    for item in recurring:

        amount = item[3]

        transaction_type = item[4]


        if transaction_type == "Income":

            projected_income += amount

        else:

            projected_expenses += amount



    return {
        "income": projected_income,
        "expenses": projected_expenses,
        "net": projected_income - projected_expenses
    }

# ==========================
# DASHBOARD INTELLIGENCE
# ==========================


def get_total_budget():

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    SELECT SUM(amount)

    FROM budgets
    """)


    result = cur.fetchone()[0]


    conn.close()


    return result if result else 0



def get_total_spending():

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



def get_budget_remaining():

    return (
        get_total_budget()
        -
        get_total_spending()
    )



def get_upcoming_recurring():

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    SELECT *

    FROM recurring_transactions

    WHERE active = 1

    ORDER BY next_date

    LIMIT 5
    """)


    results = cur.fetchall()


    conn.close()


    return results
# ==========================
# RECEIPT FUNCTIONS
# ==========================


def add_receipt(
        transaction_id,
        vendor,
        amount,
        notes,
        file_path=""
):

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    INSERT INTO receipts
    (
        transaction_id,
        vendor,
        amount,
        date,
        file_path,
        notes
    )

    VALUES
    (
        ?,
        ?,
        ?,
        DATE('now'),
        ?,
        ?
    )

    """,
    (
        transaction_id,
        vendor,
        amount,
        file_path,
        notes
    ))


    conn.commit()

    conn.close()



def get_receipts():

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    SELECT *

    FROM receipts

    ORDER BY id DESC

    """)


    receipts = cur.fetchall()


    conn.close()


    return receipts



def delete_receipt(
        receipt_id
):

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    DELETE FROM receipts

    WHERE id = ?

    """,
    (
        receipt_id,
    ))


    conn.commit()

    conn.close()