import sqlite3

conn = sqlite3.connect("data/database/sales.db")

cursor = conn.cursor()

cursor.execute("""
SELECT DISTINCT
strftime('%Y', OrderDate)
FROM Sales
ORDER BY 1
""")

print(cursor.fetchall())

conn.close()