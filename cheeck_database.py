import sqlite3

conn = sqlite3.connect("data/finance.db")

cur = conn.cursor()

cur.execute("""
SELECT *
FROM vendor_memory
""")

rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()