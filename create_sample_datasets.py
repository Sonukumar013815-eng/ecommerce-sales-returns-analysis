"""
Generate the two standard sample datasets for the Data Analysis Dashboard:
1. sales.csv (Date, Product, Category, Quantity, Sales, Profit)
2. people_data.csv (Person_ID, Name, Age, Gender, City, Occupation, Monthly_Income_INR, Marital_Status)
"""

from pathlib import Path
import random
import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 1. SALES DATASET
# -------------------------------------------------------------
PRODUCTS = [
    {"product": "Laptop", "category": "Electronics", "unit_price": 50000, "margin": 0.20},
    {"product": "Monitor", "category": "Electronics", "unit_price": 14000, "margin": 0.22},
    {"product": "Headphones", "category": "Accessories", "unit_price": 2500, "margin": 0.30},
    {"product": "Mouse", "category": "Accessories", "unit_price": 600, "margin": 0.35},
    {"product": "Keyboard", "category": "Accessories", "unit_price": 1200, "margin": 0.28},
    {"product": "USB Drive", "category": "Accessories", "unit_price": 450, "margin": 0.40},
    {"product": "Office Chair", "category": "Furniture", "unit_price": 7500, "margin": 0.25},
    {"product": "Study Desk", "category": "Furniture", "unit_price": 11000, "margin": 0.22},
    {"product": "Bookshelf", "category": "Furniture", "unit_price": 4800, "margin": 0.24},
    {"product": "Notebook Pack", "category": "Stationery", "unit_price": 250, "margin": 0.45},
    {"product": "Pen Set", "category": "Stationery", "unit_price": 180, "margin": 0.50},
    {"product": "Desk Lamp", "category": "Furniture", "unit_price": 1500, "margin": 0.30},
]

dates = pd.date_range(start="2026-01-01", end="2026-10-15", freq="D")
sales_records = []

for i in range(250):
    p = random.choice(PRODUCTS)
    dt = random.choice(dates).strftime("%Y-%m-%d")
    qty = random.choices([1, 2, 3, 4, 5, 8, 10], weights=[0.45, 0.25, 0.15, 0.08, 0.04, 0.02, 0.01])[0]
    # small random discount or price variation
    variation = random.uniform(0.90, 1.05)
    sales = int(round(p["unit_price"] * qty * variation))
    profit = int(round(sales * p["margin"] * random.uniform(0.85, 1.15)))

    sales_records.append({
        "Date": dt,
        "Product": p["product"],
        "Category": p["category"],
        "Quantity": qty,
        "Sales": sales,
        "Profit": profit,
    })

sales_df = pd.DataFrame(sales_records).sort_values("Date").reset_index(drop=True)

# Add intentional slight missing values in a few rows to test data cleaning page
sales_df.loc[12, "Quantity"] = np.nan
sales_df.loc[34, "Profit"] = np.nan
# Add 2 duplicate rows to test duplicate cleaning
dup_rows = sales_df.iloc[[5, 20]].copy()
sales_df = pd.concat([sales_df, dup_rows], ignore_index=True)

sales_df.to_csv(BASE_DIR / "sales.csv", index=False)
sales_df.to_csv(DATA_DIR / "sales.csv", index=False)
print(f"sales.csv created with {len(sales_df)} rows at {BASE_DIR / 'sales.csv'}")

# -------------------------------------------------------------
# 2. PEOPLE DATASET
# -------------------------------------------------------------
FIRST_NAMES = [
    "Aarav", "Aditi", "Ananya", "Arjun", "Deepak", "Dev", "Isha", "Kavita", "Kiran",
    "Manish", "Neha", "Nikhil", "Pooja", "Priya", "Rahul", "Rakesh", "Riya", "Rohan",
    "Rohit", "Sameer", "Sanjay", "Shreya", "Sneha", "Sunil", "Suresh", "Tanvi", "Varun",
    "Vikram", "Yash", "Zoya", "Amit", "Kunal", "Meera", "Swati", "Divya", "Gaurav"
]
LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Gupta", "Mehta", "Singh", "Kumar", "Iyer", "Nair",
    "Reddy", "Chopra", "Joshi", "Bose", "Das", "Rao", "Mishra", "Kulkarni", "Deshmukh"
]

CITIES = ["New Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Pune", "Jaipur", "Chennai", "Kolkata", "Ahmedabad", "Chandigarh"]
OCCUPATIONS = [
    {"title": "Software Engineer", "base_income": 85000, "std": 25000},
    {"title": "Data Analyst", "base_income": 65000, "std": 18000},
    {"title": "Doctor", "base_income": 120000, "std": 35000},
    {"title": "Teacher", "base_income": 42000, "std": 12000},
    {"title": "Architect", "base_income": 75000, "std": 20000},
    {"title": "Accountant", "base_income": 48000, "std": 14000},
    {"title": "Graphic Designer", "base_income": 45000, "std": 12000},
    {"title": "Marketing Manager", "base_income": 78000, "std": 22000},
    {"title": "Civil Engineer", "base_income": 58000, "std": 16000},
    {"title": "Product Manager", "base_income": 110000, "std": 30000},
]
MARITAL_STATUSES = ["Single", "Married", "Divorced"]

people_records = []
for i in range(1, 201):
    pid = f"P-{1000 + i}"
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    age = int(np.clip(np.random.normal(33, 9), 21, 62))
    gender = random.choices(["Male", "Female", "Other"], weights=[0.49, 0.49, 0.02])[0]
    city = random.choice(CITIES)
    occ = random.choice(OCCUPATIONS)
    
    # Income has positive correlation with age/experience
    exp_factor = 1.0 + (age - 21) * 0.025
    income = int(np.clip(np.random.normal(occ["base_income"] * exp_factor, occ["std"]), 22000, 260000))
    marital = "Married" if age > 29 and random.random() < 0.72 else ("Single" if age < 28 else random.choice(MARITAL_STATUSES))

    people_records.append({
        "Person_ID": pid,
        "Name": name,
        "Age": age,
        "Gender": gender,
        "City": city,
        "Occupation": occ["title"],
        "Monthly_Income_INR": income,
        "Marital_Status": marital,
    })

people_df = pd.DataFrame(people_records)

# Introduce a couple intentional missing values to demonstrate data cleaning capabilities
people_df.loc[15, "Age"] = np.nan
people_df.loc[42, "Occupation"] = np.nan
people_df.loc[88, "Monthly_Income_INR"] = np.nan
# Add 2 duplicate rows to test duplicate cleaning
dup_p = people_df.iloc[[10, 30]].copy()
people_df = pd.concat([people_df, dup_p], ignore_index=True)

people_df.to_csv(BASE_DIR / "people_data.csv", index=False)
people_df.to_csv(DATA_DIR / "people_data.csv", index=False)
print(f"people_data.csv created with {len(people_df)} rows at {BASE_DIR / 'people_data.csv'}")
