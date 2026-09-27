-- Monthly Sales Trend

SELECT

strftime('%Y',OrderDate) Year,

strftime('%m',OrderDate) Month,

ROUND(SUM(SalesAmount),2) Sales,

ROUND(SUM(Profit),2) Profit

FROM Sales

GROUP BY Year,Month

ORDER BY Year,Month;



-- Payment Mode

SELECT

PaymentMode,

COUNT(*) Orders,

ROUND(SUM(SalesAmount),2) Sales

FROM Sales

GROUP BY PaymentMode;