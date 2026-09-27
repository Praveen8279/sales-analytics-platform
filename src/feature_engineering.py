import sqlite3
import pandas as pd
import numpy as np
from config import DATABASE_FILE

# ===========================================
# Connect Database
# ===========================================

conn = sqlite3.connect(DATABASE_FILE)

print("Connected Successfully")

# ===========================================
# Read Sales Data
# ===========================================

df = pd.read_sql("SELECT * FROM Sales", conn)

print("Rows Loaded :", len(df))

# ===========================================
# Convert Date
# ===========================================

df["OrderDate"] = pd.to_datetime(df["OrderDate"])

# ===========================================
# Profit Margin
# ===========================================

df["ProfitMargin"] = (
    df["Profit"] /
    df["SalesAmount"]
) * 100

# ===========================================
# Revenue Category
# ===========================================

df["RevenueCategory"] = pd.cut(

    df["SalesAmount"],

    bins=[
        0,
        1000,
        5000,
        10000,
        np.inf
    ],

    labels=[
        "Low",
        "Medium",
        "High",
        "Premium"
    ]

)

# ===========================================
# Profit Category
# ===========================================

df["ProfitCategory"] = pd.cut(

    df["Profit"],

    bins=[
        -100000,
        0,
        500,
        2000,
        np.inf
    ],

    labels=[
        "Loss",
        "Low",
        "Medium",
        "High"
    ]

)

# ===========================================
# Quarter
# ===========================================

df["Quarter"] = (
    "Q" +
    df["OrderDate"]
    .dt.quarter
    .astype(str)
)

# ===========================================
# Month
# ===========================================

df["Month"] = (
    df["OrderDate"]
    .dt.month_name()
)

# ===========================================
# Year
# ===========================================

df["Year"] = (
    df["OrderDate"]
    .dt.year
)

# ===========================================
# Week Number
# ===========================================

df["Week"] = (
    df["OrderDate"]
    .dt.isocalendar()
    .week
)

# ===========================================
# Day Name
# ===========================================

df["Day"] = (
    df["OrderDate"]
    .dt.day_name()
)

# ===========================================
# Weekend Flag
# ===========================================

df["Weekend"] = np.where(

    df["Day"].isin([

        "Saturday",

        "Sunday"

    ]),

    "Yes",

    "No"

)

# ===========================================
# Save Engineered Dataset
# ===========================================

output = "data/processed/sales_features.csv"

df.to_csv(

    output,

    index=False

)

print()

print("Feature Engineering Completed")

print()

print("Saved :", output)

conn.close()