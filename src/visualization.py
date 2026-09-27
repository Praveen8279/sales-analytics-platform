import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from config import DATABASE_FILE

# ==================================================
# Paths
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REPORTS_DIR = PROJECT_ROOT / "reports" / "charts"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# ==================================================
# Database Connection
# ==================================================

conn = sqlite3.connect(DATABASE_FILE)

# ==================================================
# Helper Function
# ==================================================

def save_chart(df, x, y, title, xlabel, ylabel, filename, kind="bar", rotate=45):

    plt.figure(figsize=(12, 6))

    if kind == "bar":
        plt.bar(df[x], df[y])

    elif kind == "line":
        plt.plot(df[x], df[y], marker="o")

    elif kind == "pie":
        plt.pie(df[y], labels=df[x], autopct="%1.1f%%")

    plt.title(title)

    if kind != "pie":
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=rotate)

    plt.tight_layout()

    plt.savefig(REPORTS_DIR / filename, dpi=300)

    plt.close()

# ==================================================
# Monthly Sales
# ==================================================

monthly_sales = pd.read_sql("""

SELECT

strftime('%Y-%m',OrderDate) Month,

SUM(SalesAmount) Sales

FROM Sales

GROUP BY Month

ORDER BY Month

""", conn)

save_chart(
    monthly_sales,
    "Month",
    "Sales",
    "Monthly Sales",
    "Month",
    "Sales",
    "monthly_sales.png",
    "line"
)

# ==================================================
# Monthly Profit
# ==================================================

monthly_profit = pd.read_sql("""

SELECT

strftime('%Y-%m',OrderDate) Month,

SUM(Profit) Profit

FROM Sales

GROUP BY Month

ORDER BY Month

""", conn)

save_chart(
    monthly_profit,
    "Month",
    "Profit",
    "Monthly Profit",
    "Month",
    "Profit",
    "monthly_profit.png",
    "line"
)

# ==================================================
# State Sales
# ==================================================

state_sales = pd.read_sql("""

SELECT

Customers.State,

SUM(Sales.SalesAmount) Sales

FROM Sales

JOIN Customers

ON Sales.CustomerID=Customers.CustomerID

GROUP BY Customers.State

ORDER BY Sales DESC

LIMIT 20

""", conn)

save_chart(
    state_sales,
    "State",
    "Sales",
    "Top States",
    "State",
    "Sales",
    "state_sales.png"
)

# ==================================================
# Category Sales
# ==================================================

category_sales = pd.read_sql("""

SELECT

Products.Category,

SUM(Sales.SalesAmount) Sales

FROM Sales

JOIN Products

ON Sales.ProductID=Products.ProductID

GROUP BY Products.Category

ORDER BY Sales DESC

""", conn)

save_chart(
    category_sales,
    "Category",
    "Sales",
    "Category Sales",
    "Category",
    "Sales",
    "category_sales.png"
)

# ==================================================
# Payment Mode
# ==================================================

payment = pd.read_sql("""

SELECT

PaymentMode,

COUNT(*) Orders

FROM Sales

GROUP BY PaymentMode

""", conn)

save_chart(
    payment,
    "PaymentMode",
    "Orders",
    "Payment Mode",
    "",
    "",
    "payment_mode.png",
    "pie",
    0
)

# ==================================================
# Top Customers
# ==================================================

customers = pd.read_sql("""

SELECT

CustomerID,

SUM(SalesAmount) Sales

FROM Sales

GROUP BY CustomerID

ORDER BY Sales DESC

LIMIT 10

""", conn)

save_chart(
    customers,
    "CustomerID",
    "Sales",
    "Top Customers",
    "Customer",
    "Sales",
    "top_customers.png"
)

# ==================================================
# Top Products
# ==================================================

products = pd.read_sql("""

SELECT

Products.ProductName,

SUM(Sales.SalesAmount) Sales

FROM Sales

JOIN Products

ON Sales.ProductID=Products.ProductID

GROUP BY Products.ProductName

ORDER BY Sales DESC

LIMIT 10

""", conn)

save_chart(
    products,
    "ProductName",
    "Sales",
    "Top Products",
    "Product",
    "Sales",
    "top_products.png"
)

# ==================================================
# Profit Distribution
# ==================================================

profit = pd.read_sql("""

SELECT Profit

FROM Sales

LIMIT 100000

""", conn)

plt.figure(figsize=(10,6))

plt.hist(profit["Profit"], bins=40)

plt.title("Profit Distribution")

plt.xlabel("Profit")

plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(REPORTS_DIR / "profit_distribution.png", dpi=300)

plt.close()

# ==================================================
# Sales Distribution
# ==================================================

sales = pd.read_sql("""

SELECT SalesAmount

FROM Sales

LIMIT 100000

""", conn)

plt.figure(figsize=(10,6))

plt.hist(sales["SalesAmount"], bins=40)

plt.title("Sales Distribution")

plt.xlabel("Sales")

plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(REPORTS_DIR / "sales_distribution.png", dpi=300)

plt.close()

conn.close()

print("All charts generated successfully.")