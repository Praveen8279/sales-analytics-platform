-- Category Performance

SELECT

p.Category,

ROUND(SUM(s.SalesAmount),2) Sales,

ROUND(SUM(s.Profit),2) Profit,

SUM(s.Quantity) Quantity

FROM Products p

JOIN Sales s

ON p.ProductID=s.ProductID

GROUP BY p.Category

ORDER BY Sales DESC;



-- Top Products

SELECT

p.ProductName,

ROUND(SUM(s.SalesAmount),2) Sales,

ROUND(SUM(s.Profit),2) Profit

FROM Products p

JOIN Sales s

ON p.ProductID=s.ProductID

GROUP BY p.ProductName

ORDER BY Sales DESC

LIMIT 20;