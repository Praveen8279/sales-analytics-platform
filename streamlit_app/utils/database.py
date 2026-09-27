import sqlite3
from pathlib import Path
import pandas as pd
import os

# ---------------------------------------------
# Project Base Directory
# ---------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

# ---------------------------------------------
# Database Paths
# ---------------------------------------------

LOCAL_DB_PATH = BASE_DIR / "data" / "database" / "sales.db"
DEPLOY_DB_PATH = BASE_DIR / "data" / "database" / "sales_deploy.db"

# ---------------------------------------------
# Select Database
# ---------------------------------------------
#
# Local development:
#     Uses the complete 1.5M-row database.
#
# Streamlit deployment:
#     Set USE_DEPLOYMENT_DB=true
#     Uses the smaller deployment database.
# ---------------------------------------------

USE_DEPLOYMENT_DB = os.getenv("USE_DEPLOYMENT_DB", "false").lower() == "true"

if USE_DEPLOYMENT_DB:
    DB_PATH = DEPLOY_DB_PATH
else:
    DB_PATH = LOCAL_DB_PATH


# ---------------------------------------------
# Database Connection
# ---------------------------------------------

def get_connection():
    """
    Returns a SQLite database connection.
    """
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}"
        )

    return sqlite3.connect(DB_PATH)


# ---------------------------------------------
# Execute SQL Query
# ---------------------------------------------

def run_query(query):
    """
    Executes a SQL query and returns a DataFrame.
    """
    conn = get_connection()

    try:
        df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()