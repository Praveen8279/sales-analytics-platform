import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker
from tqdm import tqdm

from config import CUSTOMER_FILE, TOTAL_CUSTOMERS, RANDOM_SEED

# --------------------------------------------
# Configuration
# --------------------------------------------

random.seed(RANDOM_SEED)

fake = Faker("en_IN")
Faker.seed(RANDOM_SEED)

# --------------------------------------------
# Lists
# --------------------------------------------

states = [
    "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar",
    "Chhattisgarh","Delhi","Goa","Gujarat","Haryana",
    "Himachal Pradesh","Jharkhand","Karnataka","Kerala",
    "Madhya Pradesh","Maharashtra","Odisha","Punjab",
    "Rajasthan","Tamil Nadu","Telangana","Uttar Pradesh",
    "Uttarakhand","West Bengal"
]

segments = [
    "Consumer",
    "Corporate",
    "Home Office"
]

loyalty = [
    "Bronze",
    "Silver",
    "Gold",
    "Platinum"
]

# --------------------------------------------
# Generate Customers
# --------------------------------------------

rows = []

start_date = datetime(2018, 1, 1)

print("Generating Customers...")

for i in tqdm(range(1, TOTAL_CUSTOMERS + 1)):

    name = fake.name()

    rows.append({

        "CustomerID": f"CUST{i:07d}",

        "CustomerName": name,

        "Gender": random.choice(["Male", "Female"]),

        "Age": random.randint(18, 70),

        "Email": fake.email(),

        "Phone": fake.phone_number(),

        "City": fake.city(),

        "State": random.choice(states),

        "CustomerSegment": random.choice(segments),

        "JoinDate": (
            start_date +
            timedelta(days=random.randint(0, 2500))
        ).strftime("%Y-%m-%d"),

        "LoyaltyStatus": random.choice(loyalty),

        "LifetimeValue": round(
            random.uniform(1000, 500000),
            2
        )

    })

# --------------------------------------------
# Save
# --------------------------------------------

df = pd.DataFrame(rows)

df.to_csv(CUSTOMER_FILE, index=False)

print("\nCustomers Generated Successfully")

print(df.head())

print("\nShape:", df.shape)