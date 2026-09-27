import streamlit as st
from datetime import datetime

from utils.database import run_query
from utils.helpers import format_currency, format_number

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Product Analytics",
    page_icon="📦",
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

st.title("📦 Product Analytics")

st.caption(
    "Product Performance Dashboard | Streamlit • SQLite • Plotly"
)

st.write(
    f"**Last Refreshed:** {datetime.now().strftime('%d %B %Y %I:%M %p')}"
)

st.markdown("---")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("🔎 Product Filters")

# ---------------- YEAR ----------------

year_df = load_data("""
SELECT DISTINCT
strftime('%Y',OrderDate) AS Year
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
strftime('%m',OrderDate) AS Month
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

# ---------------- RATING ----------------

rating_df = load_data("""
SELECT DISTINCT
CAST(Rating AS INTEGER) AS Rating
FROM Products
ORDER BY Rating
""")

selected_rating = st.sidebar.selectbox(
    "⭐ Rating",
    ["All"] + rating_df["Rating"].astype(str).tolist()
)

# =====================================================
# WHERE CLAUSE
# =====================================================

filters = []

if selected_year != "All":
    filters.append(f"strftime('%Y',S.OrderDate)='{selected_year}'")

if selected_month != "All":
    filters.append(f"strftime('%m',S.OrderDate)='{selected_month}'")

if selected_category != "All":
    filters.append(f"P.Category='{selected_category}'")

if selected_brand != "All":
    filters.append(f"P.Brand='{selected_brand}'")

if selected_rating != "All":
    filters.append(f"CAST(P.Rating AS INTEGER)={selected_rating}")

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

⭐ Rating : {selected_rating}
""")

st.markdown("---")

# =====================================================
# PRODUCT KPI SECTION
# =====================================================

kpi_query = f"""
SELECT

COUNT(DISTINCT P.ProductID) AS TotalProducts,

COUNT(DISTINCT P.Brand) AS TotalBrands,

COUNT(DISTINCT P.Category) AS TotalCategories,

AVG(P.Rating) AS AvgRating

FROM Products P

LEFT JOIN Sales S
ON P.ProductID = S.ProductID

{where_clause}
"""

with st.spinner("Loading Product KPIs..."):
    kpi = load_data(kpi_query)

total_products = kpi.iloc[0]["TotalProducts"] or 0
total_brands = kpi.iloc[0]["TotalBrands"] or 0
total_categories = kpi.iloc[0]["TotalCategories"] or 0
avg_rating = kpi.iloc[0]["AvgRating"] or 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📦 Total Products",
        format_number(total_products)
    )

with col2:
    st.metric(
        "🏷 Total Brands",
        format_number(total_brands)
    )

with col3:
    st.metric(
        "📂 Categories",
        format_number(total_categories)
    )

with col4:
    st.metric(
        "⭐ Average Rating",
        f"{avg_rating:.2f}"
    )

st.markdown("---")
from utils.charts import (
    create_line_chart,
    create_bar_chart
)

# =====================================================
# PRODUCT SALES TREND
# =====================================================

trend_query = f"""
SELECT
    strftime('%Y-%m', S.OrderDate) AS Month,
    SUM(S.SalesAmount) AS Sales
FROM Sales S
JOIN Products P
ON S.ProductID=P.ProductID

{where_clause}

GROUP BY Month
ORDER BY Month
"""

with st.spinner("Loading Product Sales Trend..."):
    trend_df = load_data(trend_query)

if trend_df.empty:

    st.warning("No product sales data available.")

else:

    fig = create_line_chart(
        trend_df,
        x="Month",
        y="Sales",
        title="📈 Product Sales Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
col1, col2 = st.columns(2)
product_query = f"""
SELECT
    P.ProductName,
    SUM(S.SalesAmount) AS Sales
FROM Sales S
JOIN Products P
ON S.ProductID=P.ProductID

{where_clause}

GROUP BY P.ProductName
ORDER BY Sales DESC
LIMIT 10
"""

product_df = load_data(product_query)

with col1:

    if product_df.empty:

        st.warning("No product data.")

    else:

        fig = create_bar_chart(
            product_df,
            x="ProductName",
            y="Sales",
            title="🏆 Top 10 Products"
        )

        st.plotly_chart(fig, use_container_width=True)
        category_query = f"""
SELECT
    P.Category,
    SUM(S.SalesAmount) AS Sales
FROM Sales S
JOIN Products P
ON S.ProductID=P.ProductID

{where_clause}

GROUP BY P.Category
ORDER BY Sales DESC
"""

category_df = load_data(category_query)

with col2:

    if category_df.empty:

        st.warning("No category data.")

    else:

        fig = create_bar_chart(
            category_df,
            x="Category",
            y="Sales",
            title="📦 Category Performance"
        )

        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
col1, col2 = st.columns(2)
brand_query = f"""
SELECT
    P.Brand,
    SUM(S.SalesAmount) AS Sales
FROM Sales S
JOIN Products P
ON S.ProductID=P.ProductID

{where_clause}

GROUP BY P.Brand
ORDER BY Sales DESC
LIMIT 10
"""

brand_df = load_data(brand_query)

with col1:

    if brand_df.empty:

        st.warning("No brand data.")

    else:

        fig = create_bar_chart(
            brand_df,
            x="Brand",
            y="Sales",
            title="🏷️ Brand Performance"
        )

        st.plotly_chart(fig, use_container_width=True)
        subcategory_query = f"""
SELECT
    P.SubCategory,
    SUM(S.SalesAmount) AS Sales
FROM Sales S
JOIN Products P
ON S.ProductID=P.ProductID

{where_clause}

GROUP BY P.SubCategory
ORDER BY Sales DESC
LIMIT 10
"""

subcategory_df = load_data(subcategory_query)

with col2:

    if subcategory_df.empty:

        st.warning("No subcategory data.")

    else:

        fig = create_bar_chart(
            subcategory_df,
            x="SubCategory",
            y="Sales",
            title="📂 Subcategory Performance"
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

st.caption(
    f"📅 Last Refreshed: {datetime.now().strftime('%d %B %Y • %I:%M %p')}"
)

st.caption("Powered by Streamlit • SQLite • Plotly")