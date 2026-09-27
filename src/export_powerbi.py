import sqlite3
from pathlib import Path
import pandas as pd
from config import DATABASE_FILE

# ===========================================
# Paths
# ===========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

EXPORT_FOLDER = PROJECT_ROOT / "powerbi"

EXPORT_FOLDER.mkdir(exist_ok=True)

# ===========================================
# Database Connection
# ===========================================

conn = sqlite3.connect(DATABASE_FILE)

print("Connected Successfully")

# ===========================================
# Export Fact Table
# ===========================================

sales = pd.read_sql("SELECT * FROM Sales", conn)

sales.to_csv(
    EXPORT_FOLDER / "FactSales.csv",
    index=False
)

print("FactSales Exported")

# ===========================================
# Export Customers
# ===========================================

customers = pd.read_sql(
    "SELECT * FROM Customers",
    conn
)

customers.to_csv(
    EXPORT_FOLDER / "DimCustomer.csv",
    index=False
)

print("DimCustomer Exported")

# ===========================================
# Export Products
# ===========================================

products = pd.read_sql(
    "SELECT * FROM Products",
    conn
)

products.to_csv(
    EXPORT_FOLDER / "DimProduct.csv",
    index=False
)

print("DimProduct Exported")

# ===========================================
# Export Employees
# ===========================================

employees = pd.read_sql(
    "SELECT * FROM Employees",
    conn
)

employees.to_csv(
    EXPORT_FOLDER / "DimEmployee.csv",
    index=False
)

print("DimEmployee Exported")

# ===========================================
# Export Calendar
# ===========================================

calendar = pd.read_sql(
    "SELECT * FROM Calendar",
    conn
)

calendar.to_csv(
    EXPORT_FOLDER / "DimCalendar.csv",
    index=False
)

print("DimCalendar Exported")

conn.close()

print("\nPower BI Files Ready")