from utils.database import run_query

df = run_query("SELECT COUNT(*) AS TotalSales FROM Sales")

print(df)