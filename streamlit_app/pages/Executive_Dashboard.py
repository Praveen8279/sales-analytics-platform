import streamlit as st
import pandas as pd
from datetime import datetime

from utils.database import run_query
from utils.helpers import format_currency, format_number
from utils.charts import (
    create_line_chart,
    create_bar_chart,
    create_pie_chart
)

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LOAD CSS
# =====================================================

with open("streamlit_app/assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# =====================================================
# CACHE DATABASE QUERY
# =====================================================

@st.cache_data
def load_data(query):
    return run_query(query)

# =====================================================
# DASHBOARD HEADER
# =====================================================

st.title("📊 Executive Dashboard")
st.markdown(
"""
Welcome to the Executive Dashboard.

Use the filters on the left to explore Sales, Profit, Orders and Customer performance interactively.
"""
)

st.caption(
    "Professional Sales Analytics Dashboard | Streamlit • SQLite • Plotly"
)

st.write(
    f"**Last Refreshed:** {datetime.now().strftime('%d %B %Y %I:%M %p')}"
)

st.markdown("---")

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("🔎 Dashboard Filters")
st.sidebar.markdown("---")

st.sidebar.caption(
    "Select one or more filters to update the dashboard."
)

# -----------------------
# Year
# -----------------------

year_df = load_data("""
SELECT DISTINCT
strftime('%Y', OrderDate) AS Year
FROM Sales
ORDER BY Year
""")

selected_year = st.sidebar.selectbox(
    "📅 Year",
    ["All"] + year_df["Year"].tolist()
)

# -----------------------
# Month
# -----------------------

month_df = load_data("""
SELECT DISTINCT
strftime('%m', OrderDate) AS Month
FROM Sales
ORDER BY Month
""")

selected_month = st.sidebar.selectbox(
    "📆 Month",
    ["All"] + month_df["Month"].tolist()
)

# -----------------------
# Category
# -----------------------

category_df = load_data("""
SELECT DISTINCT
Category
FROM Products
ORDER BY Category
""")

selected_category = st.sidebar.selectbox(
    "📦 Category",
    ["All"] + category_df["Category"].tolist()
)

# -----------------------
# Brand
# -----------------------

brand_df = load_data("""
SELECT DISTINCT
Brand
FROM Products
ORDER BY Brand
""")

selected_brand = st.sidebar.selectbox(
    "🏷️ Brand",
    ["All"] + brand_df["Brand"].tolist()
)

# -----------------------
# Payment Mode
# -----------------------

payment_df = load_data("""
SELECT DISTINCT
PaymentMode
FROM Sales
ORDER BY PaymentMode
""")

selected_payment = st.sidebar.selectbox(
    "💳 Payment Mode",
    ["All"] + payment_df["PaymentMode"].tolist()
)

# =====================================================
# SQL FILTERS
# =====================================================

filters = []

if selected_year != "All":
    filters.append(
        f"strftime('%Y', S.OrderDate) = '{selected_year}'"
    )

if selected_month != "All":
    filters.append(
        f"strftime('%m', S.OrderDate) = '{selected_month}'"
    )

if selected_category != "All":
    filters.append(
        f"P.Category = '{selected_category}'"
    )

if selected_brand != "All":
    filters.append(
        f"P.Brand = '{selected_brand}'"
    )

if selected_payment != "All":
    filters.append(
        f"S.PaymentMode = '{selected_payment}'"
    )

where_clause = ""

if filters:
    where_clause = "WHERE " + " AND ".join(filters)

st.info(
    f"""
**Selected Filters**

📅 Year: {selected_year}

📆 Month: {selected_month}

📦 Category: {selected_category}

🏷️ Brand: {selected_brand}

💳 Payment Mode: {selected_payment}
"""
)

st.markdown("---")

# =====================================================
# KPI SECTION
# =====================================================

kpi_query = f"""
SELECT
    SUM(S.SalesAmount) AS TotalSales,
    SUM(S.Profit) AS TotalProfit,
    COUNT(S.OrderID) AS TotalOrders,
    COUNT(DISTINCT S.CustomerID) AS TotalCustomers
FROM Sales S
JOIN Products P
ON S.ProductID = P.ProductID
{where_clause}
"""
with st.spinner("Loading Executive Dashboard..."):
    kpi = load_data(kpi_query)

total_sales = kpi.iloc[0]["TotalSales"] or 0
total_profit = kpi.iloc[0]["TotalProfit"] or 0
total_orders = kpi.iloc[0]["TotalOrders"] or 0
total_customers = kpi.iloc[0]["TotalCustomers"] or 0

profit_margin = (
    (total_profit / total_sales) * 100
    if total_sales > 0 else 0
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="💰 Total Sales",
        value=format_currency(total_sales)
    )

with col2:
    st.metric(
        label="📈 Total Profit",
        value=format_currency(total_profit)
    )

with col3:
    st.metric(
        label="🛒 Total Orders",
        value=format_number(total_orders)
    )

with col4:
    st.metric(
        label="👥 Customers",
        value=format_number(total_customers)
    )

with col5:
    st.metric(
        label="📊 Profit Margin",
        value=f"{profit_margin:.2f}%"
    )

st.markdown("---")

# =====================================================
# MONTHLY SALES TREND
# =====================================================

sales_query = f"""
SELECT
    strftime('%Y-%m', S.OrderDate) AS Month,
    SUM(S.SalesAmount) AS Sales
FROM Sales S
JOIN Products P
ON S.ProductID = P.ProductID
{where_clause}
GROUP BY Month
ORDER BY Month
"""
with st.spinner("Loading Sales Trend..."):
    sales_df = load_data(sales_query)

if sales_df.empty:

    st.warning("No sales data found for the selected filters.")

else:

    fig = create_line_chart(
        sales_df,
        x="Month",
        y="Sales",
        title="📈 Monthly Sales Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

# =====================================================
# PAYMENT MODE
# =====================================================

payment_query = f"""
SELECT
    S.PaymentMode,
    SUM(S.SalesAmount) AS Sales
FROM Sales S
JOIN Products P
ON S.ProductID = P.ProductID
{where_clause}
GROUP BY S.PaymentMode
ORDER BY Sales DESC
"""
with st.spinner("Loading Payment Analysis..."):
    payment_df = load_data(payment_query)
with col1:
    if payment_df.empty:

        st.warning("No payment data available.")

    else:

        fig = create_pie_chart(
            payment_df,
            names="PaymentMode",
            values="Sales",
            title="🍩 Payment Mode Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)
# =====================================================
# TOP CATEGORIES
# =====================================================

category_query = f"""
SELECT
    P.Category,
    SUM(S.SalesAmount) AS Sales
FROM Sales S
JOIN Products P
ON S.ProductID = P.ProductID
{where_clause}
GROUP BY P.Category
ORDER BY Sales DESC
LIMIT 10
"""
with st.spinner("Loading Category Analysis..."):
    category_df = load_data(category_query)


with col2:
    if category_df.empty:
        st.warning("No category data available.")
    else:
        fig = create_bar_chart(
            category_df,
            x="Category",
            y="Sales",
            title="📦 Top Categories"
        )
        st.plotly_chart(fig, use_container_width=True)


st.markdown("---")

col1, col2 = st.columns([3,1])

with col1:

    st.caption(
        f"📅 Last Refreshed: {datetime.now().strftime('%d %B %Y • %I:%M %p')}"
    )

    st.caption(
        "Powered by Streamlit • SQLite • Plotly"
    )

with col2:

    st.caption("Version 1.0")