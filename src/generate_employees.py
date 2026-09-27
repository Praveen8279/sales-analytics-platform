import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

from config import EMPLOYEE_FILE, TOTAL_EMPLOYEES, RANDOM_SEED

# ======================================
# Configuration
# ======================================

random.seed(RANDOM_SEED)

fake = Faker("en_IN")
Faker.seed(RANDOM_SEED)

# ======================================
# Departments
# ======================================

departments = [
    "Sales",
    "Marketing",
    "Finance",
    "Operations",
    "HR",
    "IT",
    "Customer Support"
]

designations = [
    "Executive",
    "Senior Executive",
    "Team Leader",
    "Assistant Manager",
    "Manager",
    "Senior Manager"
]

regions = [
    "North",
    "South",
    "East",
    "West",
    "Central"
]

states = [
    "Delhi",
    "Uttar Pradesh",
    "Bihar",
    "Maharashtra",
    "Karnataka",
    "Tamil Nadu",
    "Punjab",
    "Rajasthan",
    "Gujarat",
    "West Bengal"
]

# ======================================
# Generate Employees
# ======================================

rows = []

start_date = datetime(2016, 1, 1)

print("Generating Employees...")

for i in range(1, TOTAL_EMPLOYEES + 1):

    join_date = start_date + timedelta(
        days=random.randint(0, 3500)
    )

    rows.append({

        "EmployeeID": f"EMP{i:05d}",

        "EmployeeName": fake.name(),

        "Gender": random.choice(["Male", "Female"]),

        "Department": random.choice(departments),

        "Designation": random.choice(designations),

        "Manager": fake.name(),

        "Region": random.choice(regions),

        "State": random.choice(states),

        "Salary": random.randint(25000, 180000),

        "JoiningDate": join_date.strftime("%Y-%m-%d"),

        "PerformanceRating": round(
            random.uniform(2.5, 5.0),
            1
        )

    })

# ======================================
# Save
# ======================================

df = pd.DataFrame(rows)

df.to_csv(EMPLOYEE_FILE, index=False)

print("\nEmployees Generated Successfully")

print(df.head())

print()

print("Total Employees:", len(df))