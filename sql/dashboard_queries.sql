-- Dashboard Summary

SELECT

COUNT(*) Orders,

SUM(Quantity) Quantity,

ROUND(SUM(SalesAmount),2) Sales,

ROUND(SUM(Profit),2) Profit,

ROUND(AVG(SalesAmount),2) AOV

FROM Sales;



-- Top States

SELECT

c.State,

ROUND(SUM(s.SalesAmount),2) Sales,

ROUND(SUM(s.Profit),2) Profit

FROM Customers c

JOIN Sales s

ON c.CustomerID=s.CustomerID

GROUP BY c.State

ORDER BY Sales DESC;