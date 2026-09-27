CREATE VIEW SalesSummary AS

SELECT

OrderID,

CustomerID,

ProductID,

EmployeeID,

OrderDate,

Quantity,

SalesAmount,

Profit,

PaymentMode,

OrderStatus

FROM Sales;



CREATE VIEW CustomerSales AS

SELECT

CustomerID,

SUM(SalesAmount) TotalSales,

SUM(Profit) TotalProfit

FROM Sales

GROUP BY CustomerID;