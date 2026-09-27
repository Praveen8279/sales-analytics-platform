import random
from datetime import timedelta

import pandas as pd
from tqdm import tqdm

from config import (
    CUSTOMER_FILE,
    PRODUCT_FILE,
    EMPLOYEE_FILE,
    SALES_FILE,
    TOTAL_SALES,
    RANDOM_SEED,
)

random.seed(RANDOM_SEED)

# ============================================
# Load Dimension Tables
# ============================================

customers = pd.read_csv(CUSTOMER_FILE)
products = pd.read_csv(PRODUCT_FILE)
employees = pd.read_csv(EMPLOYEE_FILE)

customer_ids = customers["CustomerID"].tolist()

employee_ids = employees["EmployeeID"].tolist()

payment_modes = [
    "UPI",
    "COD",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "EMI"
]

order_status = [
    "Delivered",
    "Cancelled",
    "Returned"
]

shipping_mode = [
    "Standard",
    "Express",
    "Same Day"
]

# ============================================
# Configuration
# ============================================

CHUNK_SIZE = 100000

header_written = False

print("Generating Sales Data...")

# ============================================
# Generate Sales
# ============================================

for start in tqdm(range(0, TOTAL_SALES, CHUNK_SIZE)):

    end = min(start + CHUNK_SIZE, TOTAL_SALES)

    rows = []

    for i in range(start, end):

        product = products.sample(1).iloc[0]

        quantity = random.randint(1, 10)

        selling_price = float(product["SellingPrice"])

        cost_price = float(product["CostPrice"])

        discount = random.choice([0, 5, 10, 15, 20, 25])

        gross_sales = quantity * selling_price

        discount_amount = gross_sales * discount / 100

        sales_amount = gross_sales - discount_amount

        profit = sales_amount - (quantity * cost_price)

        shipping = random.randint(40, 500)

        order_date = (
            pd.Timestamp("2019-01-01")
            + timedelta(days=random.randint(0, 2200))
        )

        delivery_date = (
            order_date
            + timedelta(days=random.randint(1, 10))
        )

        rows.append({

            "OrderID": f"ORD{i+1:09d}",

            "CustomerID": random.choice(customer_ids),

            "EmployeeID": random.choice(employee_ids),

            "ProductID": product["ProductID"],

            "OrderDate": order_date,

            "DeliveryDate": delivery_date,

            "Quantity": quantity,

            "CostPrice": cost_price,

            "SellingPrice": selling_price,

            "Discount": discount,

            "SalesAmount": round(sales_amount, 2),

            "Profit": round(profit, 2),

            "ShippingCost": shipping,

            "PaymentMode": random.choice(payment_modes),

            "OrderStatus": random.choice(order_status),

            "ShippingMode": random.choice(shipping_mode)

        })

    df = pd.DataFrame(rows)

    df.to_csv(

        SALES_FILE,

        mode="a",

        index=False,

        header=not header_written

    )

    header_written = True

print("\nSales Data Generated Successfully")