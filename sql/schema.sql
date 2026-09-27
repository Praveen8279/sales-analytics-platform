-- ===========================================
-- Customers Table
-- ===========================================

CREATE TABLE Customers (
    CustomerID TEXT PRIMARY KEY,
    CustomerName TEXT,
    Gender TEXT,
    Age INTEGER,
    Email TEXT,
    Phone TEXT,
    City TEXT,
    State TEXT,
    CustomerSegment TEXT,
    JoinDate DATE,
    LoyaltyStatus TEXT,
    LifetimeValue REAL
);

-- ===========================================
-- Products Table
-- ===========================================

CREATE TABLE Products (
    ProductID TEXT PRIMARY KEY,
    Category TEXT,
    SubCategory TEXT,
    ProductName TEXT,
    Brand TEXT,
    Supplier TEXT,
    CostPrice REAL,
    SellingPrice REAL,
    Stock INTEGER,
    Rating REAL
);

-- ===========================================
-- Employees Table
-- ===========================================

CREATE TABLE Employees (
    EmployeeID TEXT PRIMARY KEY,
    EmployeeName TEXT,
    Gender TEXT,
    Department TEXT,
    Designation TEXT,
    Manager TEXT,
    Region TEXT,
    State TEXT,
    Salary REAL,
    JoiningDate DATE,
    PerformanceRating REAL
);

-- ===========================================
-- Calendar Table
-- ===========================================

CREATE TABLE Calendar (
    Date DATE,
    DateKey INTEGER,
    Day INTEGER,
    DayName TEXT,
    Week INTEGER,
    Month INTEGER,
    MonthName TEXT,
    Quarter TEXT,
    Year INTEGER,
    IsWeekend BOOLEAN,
    FinancialYear TEXT,
    FinancialQuarter TEXT
);

-- ===========================================
-- Sales Table
-- ===========================================

CREATE TABLE Sales (
    OrderID TEXT PRIMARY KEY,
    CustomerID TEXT,
    EmployeeID TEXT,
    ProductID TEXT,
    OrderDate DATE,
    DeliveryDate DATE,
    Quantity INTEGER,
    CostPrice REAL,
    SellingPrice REAL,
    Discount REAL,
    SalesAmount REAL,
    Profit REAL,
    ShippingCost REAL,
    PaymentMode TEXT,
    OrderStatus TEXT,
    ShippingMode TEXT
);