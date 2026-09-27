from datetime import datetime
import pandas as pd

from config import CALENDAR_FILE

# ============================================
# Date Range
# ============================================

START_DATE = "2018-01-01"

END_DATE = "2030-12-31"

# ============================================
# Create Date Range
# ============================================

dates = pd.date_range(
    start=START_DATE,
    end=END_DATE,
    freq="D"
)

df = pd.DataFrame()

df["Date"] = dates

# ============================================
# Basic Date Information
# ============================================

df["DateKey"] = df["Date"].dt.strftime("%Y%m%d").astype(int)

df["Day"] = df["Date"].dt.day

df["DayName"] = df["Date"].dt.day_name()

df["Week"] = df["Date"].dt.isocalendar().week.astype(int)

df["Month"] = df["Date"].dt.month

df["MonthName"] = df["Date"].dt.month_name()

df["Quarter"] = "Q" + df["Date"].dt.quarter.astype(str)

df["Year"] = df["Date"].dt.year

# ============================================
# Weekend
# ============================================

df["IsWeekend"] = df["DayName"].isin(
    ["Saturday", "Sunday"]
)

# ============================================
# Financial Year (India)
# ============================================

def financial_year(date):

    if date.month >= 4:

        return f"{date.year}-{date.year+1}"

    else:

        return f"{date.year-1}-{date.year}"


df["FinancialYear"] = df["Date"].apply(
    financial_year
)

# ============================================
# Financial Quarter
# ============================================

def financial_quarter(month):

    if month in [4,5,6]:
        return "Q1"

    if month in [7,8,9]:
        return "Q2"

    if month in [10,11,12]:
        return "Q3"

    return "Q4"

df["FinancialQuarter"] = df["Month"].apply(
    financial_quarter
)

# ============================================
# Save
# ============================================

df.to_csv(
    CALENDAR_FILE,
    index=False
)

print("="*60)

print("Calendar Generated Successfully")

print(df.head())

print()

print("Total Days :",len(df))

print("="*60)