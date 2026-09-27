import sqlite3
import pandas as pd

from config import DATABASE_FILE


class SalesAnalytics:
    """
    Business Analytics Engine
    """

    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_FILE)

    # ------------------------------------------
    # Load Complete Sales Data
    # ------------------------------------------

    def load_data(self):

        query = """
        SELECT *
        FROM Sales
        """

        return pd.read_sql(query, self.conn)

    # ------------------------------------------
    # Total Sales
    # ------------------------------------------

    def total_sales(self):

        query = """
        SELECT
            ROUND(SUM(SalesAmount),2) AS TotalSales
        FROM Sales
        """

        return pd.read_sql(query, self.conn)

    # ------------------------------------------
    # Total Profit
    # ------------------------------------------

    def total_profit(self):

        query = """
        SELECT
            ROUND(SUM(Profit),2) AS TotalProfit
        FROM Sales
        """

        return pd.read_sql(query, self.conn)

    # ------------------------------------------
    # Total Orders
    # ------------------------------------------

    def total_orders(self):

        query = """
        SELECT
            COUNT(*) AS TotalOrders
        FROM Sales
        """

        return pd.read_sql(query, self.conn)

    # ------------------------------------------
    # Total Quantity
    # ------------------------------------------

    def total_quantity(self):

        query = """
        SELECT
            SUM(Quantity) AS TotalQuantity
        FROM Sales
        """

        return pd.read_sql(query, self.conn)

    # ------------------------------------------
    # Average Order Value
    # ------------------------------------------

    def average_order_value(self):

        query = """
        SELECT
            ROUND(AVG(SalesAmount),2) AS AverageOrderValue
        FROM Sales
        """

        return pd.read_sql(query, self.conn)

    # ------------------------------------------
    # Profit Margin
    # ------------------------------------------

    def profit_margin(self):

        query = """
        SELECT
            ROUND(
                SUM(Profit)*100.0/
                SUM(SalesAmount),
            2) AS ProfitMargin
        FROM Sales
        """

        return pd.read_sql(query, self.conn)

    # ------------------------------------------
    # Dashboard Summary
    # ------------------------------------------

    def dashboard_summary(self):

        query = """
        SELECT

        COUNT(*) AS TotalOrders,

        SUM(Quantity) AS TotalQuantity,

        ROUND(SUM(SalesAmount),2) AS TotalSales,

        ROUND(SUM(Profit),2) AS TotalProfit,

        ROUND(AVG(SalesAmount),2) AS AverageOrderValue

        FROM Sales
        """

        return pd.read_sql(query, self.conn)
    
        # ------------------------------------------
    # Monthly Sales
    # ------------------------------------------

    def monthly_sales(self):

        query = """
        SELECT

            strftime('%Y', OrderDate) AS Year,

            strftime('%m', OrderDate) AS Month,

            ROUND(SUM(SalesAmount),2) AS TotalSales

        FROM Sales

        GROUP BY Year, Month

        ORDER BY Year, Month
        """

        return pd.read_sql(query, self.conn)
    
        # ------------------------------------------
    # Monthly Profit
    # ------------------------------------------

    def monthly_profit(self):

        query = """
        SELECT

            strftime('%Y', OrderDate) AS Year,

            strftime('%m', OrderDate) AS Month,

            ROUND(SUM(Profit),2) AS TotalProfit

        FROM Sales

        GROUP BY Year, Month

        ORDER BY Year, Month
        """

        return pd.read_sql(query, self.conn)

            # ------------------------------------------
    # State-wise Sales
    # ------------------------------------------

    def state_sales(self):

        query = """
        SELECT

            c.State,

            ROUND(SUM(s.SalesAmount),2) AS TotalSales,

            ROUND(SUM(s.Profit),2) AS TotalProfit

        FROM Sales s

        JOIN Customers c

        ON s.CustomerID = c.CustomerID

        GROUP BY c.State

        ORDER BY TotalSales DESC
        """

        return pd.read_sql(query, self.conn)
    
        # ------------------------------------------
    # Category Sales
    # ------------------------------------------

    def category_sales(self):

        query = """
        SELECT

            p.Category,

            ROUND(SUM(s.SalesAmount),2) AS TotalSales,

            ROUND(SUM(s.Profit),2) AS TotalProfit,

            SUM(s.Quantity) AS Quantity

        FROM Sales s

        JOIN Products p

        ON s.ProductID = p.ProductID

        GROUP BY p.Category

        ORDER BY TotalSales DESC
        """

        return pd.read_sql(query, self.conn)
    
        # ------------------------------------------
    # Sub Category Profit
    # ------------------------------------------

    def subcategory_profit(self):

        query = """
        SELECT

            p.SubCategory,

            ROUND(SUM(s.Profit),2) AS TotalProfit

        FROM Sales s

        JOIN Products p

        ON s.ProductID = p.ProductID

        GROUP BY p.SubCategory

        ORDER BY TotalProfit DESC
        """

        return pd.read_sql(query, self.conn)
    
        # ------------------------------------------
    # Payment Mode Analysis
    # ------------------------------------------

    def payment_mode(self):

        query = """
        SELECT

            PaymentMode,

            COUNT(*) AS Orders,

            ROUND(SUM(SalesAmount),2) AS TotalSales

        FROM Sales

        GROUP BY PaymentMode

        ORDER BY TotalSales DESC
        """

        return pd.read_sql(query, self.conn)
    
        # ------------------------------------------
    # Top 10 Customers
    # ------------------------------------------

    def top_customers(self):

        query = """
        SELECT

            c.CustomerID,
            c.CustomerName,

            ROUND(SUM(s.SalesAmount),2) AS TotalSales,

            ROUND(SUM(s.Profit),2) AS TotalProfit,

            COUNT(s.OrderID) AS TotalOrders

        FROM Sales s

        JOIN Customers c
        ON s.CustomerID = c.CustomerID

        GROUP BY c.CustomerID, c.CustomerName

        ORDER BY TotalSales DESC

        LIMIT 10
        """

        return pd.read_sql(query, self.conn)
    
        # ------------------------------------------
    # Top 10 Products
    # ------------------------------------------

    def top_products(self):

        query = """
        SELECT

            p.ProductName,

            p.Category,

            ROUND(SUM(s.SalesAmount),2) AS TotalSales,

            ROUND(SUM(s.Profit),2) AS TotalProfit,

            SUM(s.Quantity) AS QuantitySold

        FROM Sales s

        JOIN Products p

        ON s.ProductID=p.ProductID

        GROUP BY p.ProductID

        ORDER BY TotalSales DESC

        LIMIT 10
        """

        return pd.read_sql(query,self.conn)
    
        # ------------------------------------------
    # Employee Performance
    # ------------------------------------------

    def employee_sales(self):

        query = """
        SELECT

            e.EmployeeName,

            e.Department,

            ROUND(SUM(s.SalesAmount),2) AS TotalSales,

            ROUND(SUM(s.Profit),2) AS TotalProfit,

            COUNT(s.OrderID) AS Orders

        FROM Sales s

        JOIN Employees e

        ON s.EmployeeID=e.EmployeeID

        GROUP BY e.EmployeeID

        ORDER BY TotalSales DESC
        """

        return pd.read_sql(query,self.conn)
    
        # ------------------------------------------
    # Quarterly Sales
    # ------------------------------------------

    def quarterly_sales(self):

        query = """
        SELECT

            strftime('%Y',OrderDate) AS Year,

            ((CAST(strftime('%m',OrderDate) AS INTEGER)-1)/3)+1 AS Quarter,

            ROUND(SUM(SalesAmount),2) AS TotalSales,

            ROUND(SUM(Profit),2) AS TotalProfit

        FROM Sales

        GROUP BY Year,Quarter

        ORDER BY Year,Quarter
        """

        return pd.read_sql(query,self.conn)
    
        # ------------------------------------------
    # Yearly Sales
    # ------------------------------------------

    def yearly_sales(self):

        query = """
        SELECT

            strftime('%Y',OrderDate) AS Year,

            ROUND(SUM(SalesAmount),2) AS TotalSales,

            ROUND(SUM(Profit),2) AS TotalProfit

        FROM Sales

        GROUP BY Year

        ORDER BY Year
        """

        return pd.read_sql(query,self.conn)
    
        # ------------------------------------------
    # Customer Segment Analysis
    # ------------------------------------------

    def customer_segments(self):

        query = """
        SELECT

            c.CustomerSegment,

            COUNT(DISTINCT c.CustomerID) Customers,

            ROUND(SUM(s.SalesAmount),2) Sales,

            ROUND(SUM(s.Profit),2) Profit

        FROM Customers c

        JOIN Sales s

        ON c.CustomerID=s.CustomerID

        GROUP BY c.CustomerSegment

        ORDER BY Sales DESC
        """

        return pd.read_sql(query,self.conn)
    
        # ------------------------------------------
    # Brand Performance
    # ------------------------------------------

    def brand_sales(self):

        query = """
        SELECT

            p.Brand,

            ROUND(SUM(s.SalesAmount),2) AS TotalSales,

            ROUND(SUM(s.Profit),2) AS TotalProfit,

            SUM(s.Quantity) Quantity

        FROM Sales s

        JOIN Products p

        ON s.ProductID=p.ProductID

        GROUP BY p.Brand

        ORDER BY TotalSales DESC
        """

        return pd.read_sql(query,self.conn)
    
        # ------------------------------------------
    # Executive Dashboard
    # ------------------------------------------

    def executive_dashboard(self):

        return {

            "summary": self.dashboard_summary(),

            "monthly_sales": self.monthly_sales(),

            "monthly_profit": self.monthly_profit(),

            "quarterly_sales": self.quarterly_sales(),

            "state_sales": self.state_sales(),

            "category_sales": self.category_sales(),

            "subcategory_profit": self.subcategory_profit(),

            "payment_mode": self.payment_mode(),

            "top_customers": self.top_customers(),

            "top_products": self.top_products(),

            "employee_sales": self.employee_sales(),

            "customer_segments": self.customer_segments(),

            "brand_sales": self.brand_sales()

        }

    # ------------------------------------------
    # Close Connection
    # ------------------------------------------

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    analytics = SalesAnalytics()
    print("="*60)
    print("Dashboard Summary")
    print("="*60)

    print(analytics.dashboard_summary())

    print("\nMonthly Sales")
    print(analytics.monthly_sales().head())

    print("\nState Sales")
    print(analytics.state_sales().head())

    print("\nCategory Sales")
    print(analytics.category_sales().head())

    print("\nPayment Mode")
    print(analytics.payment_mode())

    print("\nTop Customers")
    print(analytics.top_customers())

    print("\nTop Products")
    print(analytics.top_products())

    print("\nEmployee Performance")
    print(analytics.employee_sales().head())

    print("\nBrand Performance")
    print(analytics.brand_sales())

    analytics.close()