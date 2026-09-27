-- Top 20 Customers

SELECT

CustomerID,

SUM(SalesAmount) AS TotalSales,

SUM(Profit) AS TotalProfit,

COUNT(OrderID) AS Orders

FROM Sales

GROUP BY CustomerID

ORDER BY TotalSales DESC

LIMIT 20;



-- Customer Segment Analysis

SELECT

c.CustomerSegment,

COUNT(DISTINCT c.CustomerID) Customers,

ROUND(SUM(s.SalesAmount),2) Sales,

ROUND(SUM(s.Profit),2) Profit

FROM Customers c

JOIN Sales s

ON c.CustomerID=s.CustomerID

GROUP BY c.CustomerSegment;