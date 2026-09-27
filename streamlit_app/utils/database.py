import sqlite3
from pathlib import Path
import pandas as pd

# ---------------------------------------------
# Database Path
# ---------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "database" / "sales.db"

# ---------------------------------------------
# Database Connection
# ---------------------------------------------

def get_connection():
    """
    Returns a SQLite database connection.
    """
    return sqlite3.connect(DB_PATH)


# ---------------------------------------------
# Execute SQL Query
# ---------------------------------------------

def run_query(query):
    """
    Executes a SQL query and returns a DataFrame.
    """
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df