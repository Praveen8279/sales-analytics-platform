import streamlit as st

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Sales Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.title("Sales Analytics Platform")

st.sidebar.success("Select a page from the sidebar.")

# ---------------------------------------------------
# Main Page
# ---------------------------------------------------

st.title("📊 Sales Analytics Platform")

st.markdown("---")

st.header("Welcome")

st.write("""
Welcome to the Sales Analytics Platform.

This project was built using:

- Python
- Streamlit
- SQLite
- Power BI
- Plotly
- Pandas

Use the navigation menu on the left to explore:

- Executive Dashboard
- Customer Analytics
- Product Analytics
- Sales & Profit Analytics
""")

st.markdown("---")

st.subheader("Project Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Customers", "500,000")

with col2:
    st.metric("Products", "2,000")

with col3:
    st.metric("Sales Records", "2,000,000")

st.markdown("---")

st.info(
    "This dashboard provides interactive business insights from the Sales Analytics Platform."
)