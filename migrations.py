import sqlite3
from datetime import datetime


# ==========================
# CURRENT DATABASE VERSION
# ==========================

CURRENT_VERSION = 1



# ==========================
# MIGRATIONS
# ==========================


def run_migrations(conn):

    create_schema_table(conn)


    version = get_database_version(conn)


    while version < CURRENT_VERSION:

        next_version = version + 1


        print(
            f"Running migration {next_version}"
        )


        apply_migration(
            conn,
            next_version
        )


        set_database_version(
            conn,
            next_version
        )


        version = next_version





# ==========================
# SCHEMA VERSION TABLE
# ==========================


def create_schema_table(conn):

    cur = conn.cursor()


    cur.execute("""
    CREATE TABLE IF NOT EXISTS schema_version(

        version INTEGER,

        applied_date TEXT
    )
    """)


    cur.execute("""
    SELECT COUNT(*)

    FROM schema_version
    """)


    count = cur.fetchone()[0]


    if count == 0:

        cur.execute("""
        INSERT INTO schema_version

        (
            version,
            applied_date
        )

        VALUES

        (
            0,
            ?
        )
        """,
        (
            datetime.now().isoformat(),
        ))


    conn.commit()





def get_database_version(conn):

    cur = conn.cursor()


    cur.execute("""
    SELECT version

    FROM schema_version

    LIMIT 1
    """)


    result = cur.fetchone()


    return result[0]





def set_database_version(
        conn,
        version
):

    cur = conn.cursor()


    cur.execute("""
    UPDATE schema_version

    SET

        version = ?,

        applied_date = ?

    """,
    (
        version,
        datetime.now().isoformat()
    ))


    conn.commit()





# ==========================
# APPLY MIGRATIONS
# ==========================


def apply_migration(
        conn,
        version
):

    if version == 1:

        migration_001(conn)





# ==========================
# MIGRATION 001
# ==========================


def migration_001(conn):

    """
    Initial migration.
    Existing tables are currently
    handled by database.py.

    This reserves the migration
    system for future updates.
    """

    pass