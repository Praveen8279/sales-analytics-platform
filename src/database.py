import sqlite3
from pathlib import Path
import pandas as pd

# ==========================================
# Project Paths
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA = PROJECT_ROOT / "data" / "raw"

DATABASE = PROJECT_ROOT / "data" / "database" / "sales.db"

DATABASE.parent.mkdir(parents=True, exist_ok=True)

# ==========================================
# Connect Database
# ==========================================

conn = sqlite3.connect(DATABASE)

print("Connected to SQLite Database")

# ==========================================
# Files to Import
# ==========================================

files = {
    "Customers": "customers.csv",
    "Products": "products.csv",
    "Employees": "employees.csv",
    "Calendar": "calendar.csv",
    "Sales": "sales.csv"
}

# ==========================================
# Import CSV Files
# ==========================================

for table_name, file_name in files.items():

    file_path = RAW_DATA / file_name

    if not file_path.exists():
        print(f"[ERROR] {file_name} not found.")
        continue

    print(f"\nImporting {file_name}...")

    df = pd.read_csv(file_path)

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    print(f"{table_name} imported successfully.")
    print(f"Rows : {len(df):,}")

# ==========================================
# Verify Tables
# ==========================================

cursor = conn.cursor()

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
)

tables = cursor.fetchall()

print("\nTables in Database")

for table in tables:
    print(table[0])

# ==========================================
# Close
# ==========================================

conn.commit()
conn.close()

print("\nDatabase Created Successfully")