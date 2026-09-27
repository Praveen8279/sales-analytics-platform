import os
import sqlite3
import pandas as pd

from config import DATABASE_FILE

# ==========================================
# Create Reports Folder
# ==========================================

REPORTS_DIR = "reports"

os.makedirs(REPORTS_DIR, exist_ok=True)

# ==========================================
# Connect Database
# ==========================================

conn = sqlite3.connect(DATABASE_FILE)

print("Connected Successfully")

# ==========================================
# Load Sales Table
# ==========================================

df = pd.read_sql("SELECT * FROM Sales", conn)

print("Rows :", len(df))
print("Columns :", len(df.columns))

# ==========================================
# Dataset Shape
# ==========================================

shape = pd.DataFrame({
    "Rows": [df.shape[0]],
    "Columns": [df.shape[1]]
})

shape.to_csv(
    f"{REPORTS_DIR}/dataset_shape.csv",
    index=False
)

# ==========================================
# Data Types
# ==========================================

dtypes = pd.DataFrame({
    "Column": df.columns,
    "Datatype": df.dtypes.astype(str)
})

dtypes.to_csv(
    f"{REPORTS_DIR}/data_types.csv",
    index=False
)

# ==========================================
# Missing Values
# ==========================================

missing = pd.DataFrame({

    "Column": df.columns,

    "MissingValues": df.isnull().sum(),

    "Percentage":
        (df.isnull().sum()/len(df))*100

})

missing.to_csv(

    f"{REPORTS_DIR}/missing_values.csv",

    index=False

)

# ==========================================
# Duplicate Rows
# ==========================================

duplicates = pd.DataFrame({

    "DuplicateRows":
    [df.duplicated().sum()]

})

duplicates.to_csv(

    f"{REPORTS_DIR}/duplicates.csv",

    index=False

)

# ==========================================
# Numeric Summary
# ==========================================

summary = df.describe()

summary.to_csv(

    f"{REPORTS_DIR}/numeric_summary.csv"

)

# ==========================================
# Correlation
# ==========================================

numeric = df.select_dtypes(include="number")

corr = numeric.corr()

corr.to_csv(

    f"{REPORTS_DIR}/correlation.csv"

)

# ==========================================
# Unique Values
# ==========================================

unique = pd.DataFrame({

    "Column": df.columns,

    "UniqueValues":

    [df[c].nunique() for c in df.columns]

})

unique.to_csv(

    f"{REPORTS_DIR}/unique_values.csv",

    index=False

)

# ==========================================
# Memory Usage
# ==========================================

memory = pd.DataFrame({

    "MemoryMB":[

        df.memory_usage(deep=True).sum()/1024/1024

    ]

})

memory.to_csv(

    f"{REPORTS_DIR}/memory_usage.csv",

    index=False

)

# ==========================================
# Save Complete Report
# ==========================================

report = pd.DataFrame({

    "Metric":[

        "Rows",

        "Columns",

        "Duplicate Rows",

        "Memory (MB)"

    ],

    "Value":[

        len(df),

        len(df.columns),

        df.duplicated().sum(),

        round(

            df.memory_usage(deep=True).sum()/1024/1024,

            2

        )

    ]

})

report.to_csv(

    f"{REPORTS_DIR}/eda_summary.csv",

    index=False

)

print("\nEDA Completed Successfully")

conn.close()