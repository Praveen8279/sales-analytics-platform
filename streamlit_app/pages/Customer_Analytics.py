import streamlit as st
from datetime import datetime

from utils.database import run_query
from utils.helpers import format_currency, format_number

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Customer Analytics",
    page_icon="👥",
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
# PAGE HEADER
# =====================================================

st.title("👥 Customer Analytics")

st.caption(
    "Customer Insights Dashboard | Streamlit • SQLite • Plotly"
)

st.write(
    f"**Last Refreshed:** {datetime.now().strftime('%d %B %Y %I:%M %p')}"
)

st.markdown("---")

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("🔎 Customer Filters")

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
# State
# -----------------------

state_df = load_data("""
SELECT DISTINCT
State
FROM Customers
ORDER BY State
""")

selected_state = st.sidebar.selectbox(
    "🏙️ State",
    ["All"] + state_df["State"].tolist()
)

# -----------------------
# Customer Segment
# -----------------------

segment_df = load_data("""
SELECT DISTINCT
CustomerSegment
FROM Customers
ORDER BY CustomerSegment
""")

selected_segment = st.sidebar.selectbox(
    "👥 Customer Segment",
    ["All"] + segment_df["CustomerSegment"].tolist()
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

if selected_state != "All":
    filters.append(
        f"C.State = '{selected_state}'"
    )

if selected_segment != "All":
    filters.append(
        f"C.CustomerSegment = '{selected_segment}'"
    )

where_clause = ""

if filters:
    where_clause = "WHERE " + " AND ".join(filters)

# =====================================================
# FILTER SUMMARY
# =====================================================

st.info(
f"""
**Selected Filters**

📅 Year : {selected_year}

📆 Month : {selected_month}

🏙️ State : {selected_state}

👥 Customer Segment : {selected_segment}
"""
)

st.markdown("---")


# =====================================================
# CUSTOMER KPI SECTION
# =====================================================
kpi_query = f"""
SELECT
    COUNT(DISTINCT C.CustomerID) AS TotalCustomers,

    COUNT(DISTINCT CASE
        WHEN strftime('%Y', C.JoinDate) = (
            SELECT MAX(strftime('%Y', JoinDate))
            FROM Customers
        )
        THEN C.CustomerID
    END) AS NewCustomers,

    COUNT(DISTINCT CASE
        WHEN C.LoyaltyStatus IN ('Gold','Platinum')
        THEN C.CustomerID
    END) AS LoyaltyCustomers,

    AVG(C.LifetimeValue) AS AvgLifetimeValue

FROM Customers C

LEFT JOIN Sales S
ON C.CustomerID = S.CustomerID

{where_clause}
"""


with st.spinner("Loading Customer KPIs..."):
    kpi = load_data(kpi_query)

total_customers = kpi.iloc[0]["TotalCustomers"] or 0
new_customers = kpi.iloc[0]["NewCustomers"] or 0
loyalty_customers = kpi.iloc[0]["LoyaltyCustomers"] or 0
avg_lifetime = kpi.iloc[0]["AvgLifetimeValue"] or 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Total Customers",
        format_number(total_customers)
    )

with col2:
    st.metric(
        "🆕 New Customers",
        format_number(new_customers)
    )

with col3:
    st.metric(
        "💎 Loyalty Customers",
        format_number(loyalty_customers)
    )

with col4:
    st.metric(
        "💰 Avg Lifetime Value",
        format_currency(avg_lifetime)
    )

st.markdown("---")

# =====================================================
# CUSTOMER GROWTH TREND
# =====================================================

from utils.charts import (
    create_line_chart,
    create_bar_chart,
    create_pie_chart
)

growth_query = f"""
SELECT
    strftime('%Y-%m', S.OrderDate) AS Month,
    COUNT(DISTINCT C.CustomerID) AS Customers
FROM Sales S
JOIN Customers C
ON S.CustomerID = C.CustomerID

{where_clause}

GROUP BY Month
ORDER BY Month
"""

with st.spinner("Loading Customer Growth Trend..."):
    growth_df = load_data(growth_query)

if growth_df.empty:

    st.warning("No customer growth data found.")

else:

    fig = create_line_chart(
        growth_df,
        x="Month",
        y="Customers",
        title="📈 Customer Growth Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)
segment_query = f"""
SELECT
    C.CustomerSegment,
    COUNT(*) AS Customers
FROM Customers C
LEFT JOIN Sales S
ON C.CustomerID=S.CustomerID

{where_clause}

GROUP BY C.CustomerSegment
ORDER BY Customers DESC
"""

segment_df = load_data(segment_query)

with col1:

    if segment_df.empty:

        st.warning("No customer segment data.")

    else:

        fig = create_pie_chart(
            segment_df,
            names="CustomerSegment",
            values="Customers",
            title="👥 Customer Segment Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)
        loyalty_query = f"""
SELECT
    LoyaltyStatus,
    COUNT(*) AS Customers
FROM Customers C
LEFT JOIN Sales S
ON C.CustomerID=S.CustomerID

{where_clause}

GROUP BY LoyaltyStatus
ORDER BY Customers DESC
"""

loyalty_df = load_data(loyalty_query)

with col2:

    if loyalty_df.empty:

        st.warning("No loyalty data.")

    else:

        fig = create_pie_chart(
            loyalty_df,
            names="LoyaltyStatus",
            values="Customers",
            title="💎 Loyalty Status Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
col1, col2 = st.columns(2)
state_query = f"""
SELECT
    C.State,
    COUNT(DISTINCT C.CustomerID) AS Customers
FROM Customers C
LEFT JOIN Sales S
ON C.CustomerID=S.CustomerID

{where_clause}

GROUP BY C.State
ORDER BY Customers DESC
LIMIT 10
"""

state_df = load_data(state_query)

with col1:

    if state_df.empty:

        st.warning("No state data.")

    else:

        fig = create_bar_chart(
            state_df,
            x="State",
            y="Customers",
            title="🏙️ Top 10 States"
        )

        st.plotly_chart(fig, use_container_width=True)
        city_query = f"""
SELECT
    C.City,
    COUNT(DISTINCT C.CustomerID) AS Customers
FROM Customers C
LEFT JOIN Sales S
ON C.CustomerID=S.CustomerID

{where_clause}

GROUP BY C.City
ORDER BY Customers DESC
LIMIT 10
"""

city_df = load_data(city_query)

with col2:

    if city_df.empty:

        st.warning("No city data.")

    else:

        fig = create_bar_chart(
            city_df,
            x="City",
            y="Customers",
            title="🌆 Top 10 Cities"
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

st.caption(
    f"📅 Last Refreshed: {datetime.now().strftime('%d %B %Y • %I:%M %p')}"
)

st.caption("Powered by Streamlit • SQLite • Plotly")