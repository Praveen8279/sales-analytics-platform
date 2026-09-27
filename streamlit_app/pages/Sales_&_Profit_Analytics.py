import streamlit as st
from datetime import datetime

from utils.database import run_query
from utils.helpers import format_currency, format_number

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Sales & Profit Analytics",
    page_icon="💹",
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
# CACHE
# =====================================================

@st.cache_data
def load_data(query):
    return run_query(query)

# =====================================================
# PAGE HEADER
# =====================================================

st.title("💹 Sales & Profit Analytics")

st.caption(
    "Sales & Profit Performance Dashboard | Streamlit • SQLite • Plotly"
)

st.write(
    f"**Last Refreshed:** {datetime.now().strftime('%d %B %Y %I:%M %p')}"
)

st.markdown("---")

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("🔎 Sales Filters")

# ---------------- YEAR ----------------

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

# ---------------- MONTH ----------------

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

# ---------------- CATEGORY ----------------

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

# ---------------- BRAND ----------------

brand_df = load_data("""
SELECT DISTINCT
Brand
FROM Products
ORDER BY Brand
""")

selected_brand = st.sidebar.selectbox(
    "🏷 Brand",
    ["All"] + brand_df["Brand"].tolist()
)

# ---------------- PAYMENT MODE ----------------

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
    filters.append(f"strftime('%Y', S.OrderDate)='{selected_year}'")

if selected_month != "All":
    filters.append(f"strftime('%m', S.OrderDate)='{selected_month}'")

if selected_category != "All":
    filters.append(f"P.Category='{selected_category}'")

if selected_brand != "All":
    filters.append(f"P.Brand='{selected_brand}'")

if selected_payment != "All":
    filters.append(f"S.PaymentMode='{selected_payment}'")

where_clause = ""

if filters:
    where_clause = "WHERE " + " AND ".join(filters)

# =====================================================
# FILTER SUMMARY
# =====================================================

st.info(f"""
**Selected Filters**

📅 Year : {selected_year}

📆 Month : {selected_month}

📦 Category : {selected_category}

🏷 Brand : {selected_brand}

💳 Payment Mode : {selected_payment}
""")

st.markdown("---")

# =====================================================
# SALES & PROFIT KPI SECTION
# =====================================================

kpi_query = f"""
SELECT

SUM(S.SalesAmount) AS TotalSales,

SUM(S.Profit) AS TotalProfit,

COUNT(S.OrderID) AS TotalOrders,

SUM(S.Discount) AS TotalDiscount

FROM Sales S

JOIN Products P
ON S.ProductID = P.ProductID

{where_clause}
"""

with st.spinner("Loading Sales & Profit KPIs..."):
    kpi = load_data(kpi_query)

total_sales = kpi.iloc[0]["TotalSales"] or 0
total_profit = kpi.iloc[0]["TotalProfit"] or 0
total_orders = kpi.iloc[0]["TotalOrders"] or 0
total_discount = kpi.iloc[0]["TotalDiscount"] or 0

profit_margin = (
    (total_profit / total_sales) * 100
    if total_sales > 0 else 0
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "💰 Total Sales",
        format_currency(total_sales)
    )

with col2:
    st.metric(
        "📈 Total Profit",
        format_currency(total_profit)
    )

with col3:
    st.metric(
        "🛒 Total Orders",
        format_number(total_orders)
    )

with col4:
    st.metric(
        "💸 Total Discount",
        format_number(total_discount)
    )

with col5:
    st.metric(
        "💹 Profit Margin",
        f"{profit_margin:.2f}%"
    )

st.markdown("---")

from utils.charts import (
    create_line_chart,
    create_bar_chart,
    create_pie_chart
)

# =====================================================
# SALES VS PROFIT TREND
# =====================================================

trend_query = f"""
SELECT
    strftime('%Y-%m', S.OrderDate) AS Month,
    SUM(S.SalesAmount) AS Sales,
    SUM(S.Profit) AS Profit
FROM Sales S
JOIN Products P
ON S.ProductID=P.ProductID

{where_clause}

GROUP BY Month
ORDER BY Month
"""

trend_df = load_data(trend_query)

if trend_df.empty:

    st.warning("No sales data available.")

else:

    fig = create_line_chart(
        trend_df,
        x="Month",
        y="Sales",
        title="📈 Monthly Sales Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
col1, col2 = st.columns(2)

profit_query = f"""
SELECT
    strftime('%Y-%m',S.OrderDate) AS Month,
    SUM(S.Profit) AS Profit
FROM Sales S
JOIN Products P
ON S.ProductID=P.ProductID

{where_clause}

GROUP BY Month
ORDER BY Month
"""

profit_df = load_data(profit_query)

with col1:

    if profit_df.empty:

        st.warning("No profit data.")

    else:

        fig = create_bar_chart(
            profit_df,
            x="Month",
            y="Profit",
            title="📊 Monthly Profit"
        )

        st.plotly_chart(fig, use_container_width=True)

        status_query = f"""
SELECT
    S.OrderStatus,
    COUNT(*) AS Orders
FROM Sales S
JOIN Products P
ON S.ProductID=P.ProductID

{where_clause}

GROUP BY S.OrderStatus
"""

status_df = load_data(status_query)

with col2:

    if status_df.empty:

        st.warning("No order status data.")

    else:

        fig = create_pie_chart(
            status_df,
            names="OrderStatus",
            values="Orders",
            title="🍩 Order Status"
        )

        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
col1, col2 = st.columns(2)

shipping_query = f"""
SELECT
    S.ShippingMode,
    COUNT(*) AS Orders
FROM Sales S
JOIN Products P
ON S.ProductID=P.ProductID

{where_clause}

GROUP BY S.ShippingMode
"""

shipping_df = load_data(shipping_query)

with col1:

    if shipping_df.empty:

        st.warning("No shipping data.")

    else:

        fig = create_pie_chart(
            shipping_df,
            names="ShippingMode",
            values="Orders",
            title="🚚 Shipping Mode"
        )

        st.plotly_chart(fig, use_container_width=True)
        payment_query = f"""
SELECT
    S.PaymentMode,
    SUM(S.SalesAmount) AS Sales
FROM Sales S
JOIN Products P
ON S.ProductID=P.ProductID

{where_clause}

GROUP BY S.PaymentMode
"""

payment_df = load_data(payment_query)

with col2:

    if payment_df.empty:

        st.warning("No payment data.")

    else:

        fig = create_bar_chart(
            payment_df,
            x="PaymentMode",
            y="Sales",
            title="💳 Payment Mode Performance"
        )

        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

discount_query = f"""
SELECT
    P.Category,
    AVG(S.Discount) AS Discount
FROM Sales S
JOIN Products P
ON S.ProductID=P.ProductID

{where_clause}

GROUP BY P.Category
ORDER BY Discount DESC
"""

discount_df = load_data(discount_query)

if discount_df.empty:

    st.warning("No discount data.")

else:

    fig = create_bar_chart(
        discount_df,
        x="Category",
        y="Discount",
        title="📉 Average Discount by Category"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

st.caption(
    f"📅 Last Refreshed: {datetime.now().strftime('%d %B %Y • %I:%M %p')}"
)

st.caption("Powered by Streamlit • SQLite • Plotly")

st.caption("© 2026 Sales Analytics Dashboard")