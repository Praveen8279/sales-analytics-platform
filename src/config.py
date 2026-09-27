from pathlib import Path

# ==========================================
# Project Directories
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

DATABASE_DIR = DATA_DIR / "database"

REPORT_DIR = BASE_DIR / "reports"

SCREENSHOT_DIR = BASE_DIR / "screenshots"

POWERBI_DIR = BASE_DIR / "powerbi"

STREAMLIT_DIR = BASE_DIR / "streamlit_app"

SQL_DIR = BASE_DIR / "sql"

NOTEBOOK_DIR = BASE_DIR / "notebooks"


# ==========================================
# Create Directories Automatically
# ==========================================

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_DIR.mkdir(parents=True, exist_ok=True)

REPORT_DIR.mkdir(parents=True, exist_ok=True)

SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# Files
# ==========================================

CUSTOMER_FILE = RAW_DATA_DIR / "customers.csv"

PRODUCT_FILE = RAW_DATA_DIR / "products.csv"

EMPLOYEE_FILE = RAW_DATA_DIR / "employees.csv"

CALENDAR_FILE = RAW_DATA_DIR / "calendar.csv"

SALES_FILE = RAW_DATA_DIR / "sales.csv"

DATABASE_FILE = DATABASE_DIR / "sales.db"


# ==========================================
# Dataset Size
# ==========================================

TOTAL_CUSTOMERS = 500_000

TOTAL_PRODUCTS = 2_000

TOTAL_EMPLOYEES = 500

TOTAL_SALES = 1_500_000


# ==========================================
# Random Seed
# ==========================================

RANDOM_SEED = 42