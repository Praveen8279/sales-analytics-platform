-- Total Sales
SELECT ROUND(SUM(SalesAmount),2) AS TotalSales
FROM Sales;

-- Total Profit
SELECT ROUND(SUM(Profit),2) AS TotalProfit
FROM Sales;

-- Total Quantity
SELECT SUM(Quantity) AS TotalQuantity
FROM Sales;

-- Total Orders
SELECT COUNT(*) AS TotalOrders
FROM Sales;

-- Average Order Value
SELECT ROUND(AVG(SalesAmount),2) AS AverageOrderValue
FROM Sales;

-- Profit Margin %
SELECT ROUND(
    SUM(Profit)*100.0/SUM(SalesAmount),
2) AS ProfitMargin
FROM Sales;