import random
import pandas as pd

from config import PRODUCT_FILE, TOTAL_PRODUCTS, RANDOM_SEED

random.seed(RANDOM_SEED)

categories = {
    "Electronics": [
        "Laptop", "Mobile", "Tablet", "Monitor",
        "Keyboard", "Mouse", "Printer", "Camera"
    ],

    "Furniture": [
        "Chair", "Table", "Sofa", "Cupboard",
        "Bed", "Desk"
    ],

    "Clothing": [
        "Shirt", "T-Shirt", "Jeans",
        "Jacket", "Shoes", "Kurta"
    ],

    "Home & Kitchen": [
        "Mixer", "Microwave", "Cookware",
        "Bottle", "Fan", "Refrigerator"
    ],

    "Sports": [
        "Cricket Bat", "Football",
        "Badminton", "Tennis Racket",
        "Gym Equipment"
    ],

    "Books": [
        "Education", "Programming",
        "Novel", "Comics",
        "Business"
    ],

    "Beauty": [
        "Face Wash",
        "Perfume",
        "Cream",
        "Shampoo"
    ],

    "Automobile": [
        "Helmet",
        "Tyre",
        "Battery",
        "Engine Oil"
    ]
}

brands = [
    "Samsung",
    "Apple",
    "HP",
    "Dell",
    "Lenovo",
    "Sony",
    "LG",
    "Nike",
    "Adidas",
    "Puma",
    "Boat",
    "MI",
    "OnePlus",
    "Philips",
    "Bajaj",
    "Prestige"
]

suppliers = [
    "ABC Traders",
    "XYZ Enterprises",
    "Global Supply",
    "Tech World",
    "India Retail",
    "Smart Distribution",
    "Prime Wholesale",
    "National Suppliers"
]

rows = []

product_number = 1

while product_number <= TOTAL_PRODUCTS:

    category = random.choice(list(categories.keys()))

    subcategory = random.choice(categories[category])

    cost_price = random.randint(100, 50000)

    selling_price = round(
        cost_price * random.uniform(1.10, 1.60),
        2
    )

    rows.append({

        "ProductID": f"PROD{product_number:05d}",

        "Category": category,

        "SubCategory": subcategory,

        "ProductName": f"{random.choice(brands)} {subcategory}",

        "Brand": random.choice(brands),

        "Supplier": random.choice(suppliers),

        "CostPrice": cost_price,

        "SellingPrice": selling_price,

        "Stock": random.randint(20, 1000),

        "Rating": round(
            random.uniform(3.0, 5.0),
            1
        )

    })

    product_number += 1

df = pd.DataFrame(rows)

df.to_csv(PRODUCT_FILE, index=False)

print("=" * 60)

print("Products Generated Successfully")

print(df.head())

print()

print("Total Products :", len(df))

print("=" * 60)