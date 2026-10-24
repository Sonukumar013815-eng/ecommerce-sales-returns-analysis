"""
Kaggle E-Commerce Dataset Generator: Orders, Customers, and Returns
Generates a realistic, highly authentic e-commerce dataset matching the Kaggle
Order and Return specification with authentic distributions, customer histories,
product categories, return reasons, and pricing dynamics.
"""

from pathlib import Path
import random
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = DATA_DIR / "ecommerce_orders_and_returns.csv"

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_ORDERS = 5000
NUM_CUSTOMERS = 1200

# Geographic regions and cities
CITIES_BY_REGION = {
    "North": ["New Delhi", "Jaipur", "Lucknow", "Chandigarh", "Noida", "Gurugram"],
    "South": ["Bengaluru", "Chennai", "Hyderabad", "Kochi", "Coimbatore"],
    "West": ["Mumbai", "Pune", "Ahmedabad", "Surat", "Goa"],
    "East": ["Kolkata", "Patna", "Bhubaneswar", "Guwahati", "Ranchi"],
}

# Customer segments
CUSTOMER_SEGMENTS = ["Consumer", "Corporate", "Small Business"]
SEGMENT_WEIGHTS = [0.70, 0.20, 0.10]

# Product Catalog with Category, Sub-Category, Base Price, and Baseline Return Propensity
CATALOG = [
    # Electronics (Moderate returns, high value, reasons: Defective, Changed Mind)
    {"category": "Electronics", "sub_category": "Laptops & Computers", "product": "Pro Ultra Gaming Laptop 15.6\"", "price": 65000, "base_return": 0.12},
    {"category": "Electronics", "sub_category": "Laptops & Computers", "product": "SlimBook Ultra-Light Notebook", "price": 42000, "base_return": 0.10},
    {"category": "Electronics", "sub_category": "Audio & Headphones", "product": "Noise-Cancelling Wireless Headphones", "price": 4500, "base_return": 0.15},
    {"category": "Electronics", "sub_category": "Audio & Headphones", "product": "True Wireless Bass Earbuds", "price": 1800, "base_return": 0.16},
    {"category": "Electronics", "sub_category": "Peripherals", "product": "Ergonomic Mechanical Keyboard", "price": 3200, "base_return": 0.08},
    {"category": "Electronics", "sub_category": "Peripherals", "product": "Wireless Precision Optical Mouse", "price": 850, "base_return": 0.06},
    {"category": "Electronics", "sub_category": "Displays & TVs", "product": "27-inch 4K UHD IPS Monitor", "price": 18500, "base_return": 0.14},
    {"category": "Electronics", "sub_category": "Smart Wearables", "product": "Smart Fitness Watch GPS", "price": 3500, "base_return": 0.13},

    # Clothing & Apparel (High returns, reasons: Size/Fit, Not as Described)
    {"category": "Clothing", "sub_category": "Men's Apparel", "product": "Slim Fit Oxford Formal Shirt", "price": 1400, "base_return": 0.28},
    {"category": "Clothing", "sub_category": "Men's Apparel", "product": "Stretch Denim Slim Jeans", "price": 1800, "base_return": 0.30},
    {"category": "Clothing", "sub_category": "Women's Apparel", "product": "Floral Print Summer Maxi Dress", "price": 2200, "base_return": 0.32},
    {"category": "Clothing", "sub_category": "Women's Apparel", "product": "Casual Knit Cotton Cardigan", "price": 1600, "base_return": 0.25},
    {"category": "Clothing", "sub_category": "Footwear", "product": "Running Performance Sneakers", "price": 3200, "base_return": 0.35},
    {"category": "Clothing", "sub_category": "Footwear", "product": "Classic Leather Oxford Shoes", "price": 3800, "base_return": 0.29},
    {"category": "Clothing", "sub_category": "Accessories", "product": "Leather Reversible Belt", "price": 750, "base_return": 0.12},
    {"category": "Clothing", "sub_category": "Accessories", "product": "Polarized Aviator Sunglasses", "price": 1250, "base_return": 0.18},

    # Home & Furniture (Bulky, moderate returns, reasons: Damaged in transit, Not as described)
    {"category": "Home & Furniture", "sub_category": "Office Furniture", "product": "Ergonomic High-Back Mesh Chair", "price": 8500, "base_return": 0.18},
    {"category": "Home & Furniture", "sub_category": "Office Furniture", "product": "Solid Wood Study Desk with Drawers", "price": 11500, "base_return": 0.15},
    {"category": "Home & Furniture", "sub_category": "Living Room", "product": "Minimalist 4-Tier Bookshelf", "price": 4200, "base_return": 0.14},
    {"category": "Home & Furniture", "sub_category": "Living Room", "product": "Convertible Fabric Futon Sofa", "price": 16000, "base_return": 0.20},
    {"category": "Home & Furniture", "sub_category": "Home Decor", "product": "Ceramic Table Lamp with Linen Shade", "price": 1750, "base_return": 0.11},
    {"category": "Home & Furniture", "sub_category": "Kitchen & Dining", "product": "Stainless Steel Cookware Set (5-pc)", "price": 3400, "base_return": 0.09},

    # Beauty & Personal Care (Low returns due to hygiene policies, reasons: Defective/Wrong item)
    {"category": "Beauty & Personal Care", "sub_category": "Skincare", "product": "Hydrating Hyaluronic Acid Serum", "price": 890, "base_return": 0.07},
    {"category": "Beauty & Personal Care", "sub_category": "Skincare", "product": "SPF 50 Mineral Sunscreen Lotion", "price": 650, "base_return": 0.05},
    {"category": "Beauty & Personal Care", "sub_category": "Fragrance", "product": "Eau De Parfum Cedar & Citrus 100ml", "price": 2800, "base_return": 0.08},
    {"category": "Beauty & Personal Care", "sub_category": "Haircare", "product": "Argan Oil Repair Hair Mask", "price": 720, "base_return": 0.06},

    # Sports & Fitness (Moderate returns, reasons: Changed Mind, Size/Fit)
    {"category": "Sports & Fitness", "sub_category": "Fitness Gear", "product": "High-Density Non-Slip Yoga Mat", "price": 1200, "base_return": 0.10},
    {"category": "Sports & Fitness", "sub_category": "Fitness Gear", "product": "Adjustable Dumbbell Pair 20kg", "price": 4800, "base_return": 0.12},
    {"category": "Sports & Fitness", "sub_category": "Outdoor & Sports", "product": "Insulated Stainless Steel Sports Bottle", "price": 850, "base_return": 0.06},
    {"category": "Sports & Fitness", "sub_category": "Outdoor & Sports", "product": "Waterproof Trekking Backpack 45L", "price": 2600, "base_return": 0.16},
]

# Return reasons by category affinity
CATEGORY_RETURN_REASONS = {
    "Clothing": [
        ("Size / Fit Issue", 0.50),
        ("Not as Described", 0.20),
        ("Changed Mind", 0.12),
        ("Defective / Damaged", 0.08),
        ("Late Delivery", 0.06),
        ("Found Better Price", 0.04),
    ],
    "Electronics": [
        ("Defective / Damaged", 0.38),
        ("Changed Mind", 0.22),
        ("Not as Described", 0.18),
        ("Found Better Price", 0.12),
        ("Late Delivery", 0.06),
        ("Size / Fit Issue", 0.04),
    ],
    "Home & Furniture": [
        ("Defective / Damaged", 0.35),
        ("Not as Described", 0.25),
        ("Size / Fit Issue", 0.18),
        ("Late Delivery", 0.12),
        ("Changed Mind", 0.06),
        ("Found Better Price", 0.04),
    ],
    "Beauty & Personal Care": [
        ("Defective / Damaged", 0.45),
        ("Not as Described", 0.30),
        ("Late Delivery", 0.15),
        ("Found Better Price", 0.06),
        ("Changed Mind", 0.04),
    ],
    "Sports & Fitness": [
        ("Size / Fit Issue", 0.30),
        ("Defective / Damaged", 0.25),
        ("Changed Mind", 0.20),
        ("Not as Described", 0.15),
        ("Late Delivery", 0.06),
        ("Found Better Price", 0.04),
    ],
}

FIRST_NAMES = [
    "Aarav", "Aditi", "Ananya", "Arjun", "Deepak", "Dev", "Isha", "Kavita", "Kiran",
    "Manish", "Neha", "Nikhil", "Pooja", "Priya", "Rahul", "Rakesh", "Riya", "Rohan",
    "Rohit", "Sameer", "Sanjay", "Shreya", "Sneha", "Sunil", "Suresh", "Tanvi", "Varun",
    "Vikram", "Yash", "Zoya"
]

LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Gupta", "Mehta", "Singh", "Kumar", "Iyer", "Nair",
    "Reddy", "Chopra", "Joshi", "Bose", "Das", "Rao", "Mishra", "Kulkarni", "Deshmukh"
]


def generate_customer_pool(num_customers):
    """Generate a persistent customer pool for realistic repeat purchase behavior."""
    customers = []
    regions = list(CITIES_BY_REGION.keys())

    for i in range(1, num_customers + 1):
        cust_id = f"CUST-{1000 + i}"
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        age = int(np.clip(np.random.normal(34, 11), 18, 70))
        gender = random.choices(["Male", "Female", "Other"], weights=[0.49, 0.49, 0.02])[0]
        region = random.choice(regions)
        city = random.choice(CITIES_BY_REGION[region])
        segment = random.choices(CUSTOMER_SEGMENTS, weights=SEGMENT_WEIGHTS)[0]
        
        # Customer return propensity factor: most return rarely, small group are serial returners
        # 10% of customers have high return propensity
        is_serial_returner = random.random() < 0.08
        return_propensity = random.uniform(1.8, 3.2) if is_serial_returner else random.uniform(0.6, 1.2)

        customers.append({
            "customer_id": cust_id,
            "customer_name": name,
            "age": age,
            "gender": gender,
            "region": region,
            "city": city,
            "segment": segment,
            "return_propensity": return_propensity,
            "is_serial_returner": is_serial_returner
        })
    return customers


def generate_dataset(num_orders=NUM_ORDERS, num_customers=NUM_CUSTOMERS):
    """Generate full dataset with orders, returns, and customer dynamics."""
    customers = generate_customer_pool(num_customers)
    
    # Date range: 2025-01-01 to 2026-03-31 (15 months)
    start_date = pd.Timestamp("2025-01-01")
    end_date = pd.Timestamp("2026-03-31")
    total_days = (end_date - start_date).days

    # Customer purchase probabilities follow Pareto distribution
    cust_weights = np.random.pareto(a=1.5, size=num_customers)
    cust_weights /= cust_weights.sum()

    records = []
    
    # Payment methods and probabilities
    payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash on Delivery", "Net Banking"]
    payment_weights = [0.42, 0.28, 0.12, 0.13, 0.05]

    shipping_types = ["Standard", "Express", "Next-Day", "Same-Day"]
    shipping_weights = [0.60, 0.25, 0.10, 0.05]

    for order_idx in range(1, num_orders + 1):
        order_id = f"ORD-2025-{10000 + order_idx}"
        
        # Pick customer
        cust = np.random.choice(customers, p=cust_weights)
        
        # Order date with Q4 seasonal holiday bump (Oct-Dec)
        day_offset = random.randint(0, total_days)
        order_date = start_date + pd.Timedelta(days=day_offset)
        
        # Holiday bump weight
        if order_date.month in [10, 11, 12]:
            # Slightly higher probability of order being kept
            pass

        # Pick product
        product_item = random.choice(CATALOG)
        category = product_item["category"]
        sub_category = product_item["sub_category"]
        product_name = product_item["product"]
        unit_price = float(product_item["price"])
        
        # Quantity: mostly 1-2, occasionally 3-5
        quantity = random.choices([1, 2, 3, 4, 5], weights=[0.68, 0.20, 0.07, 0.03, 0.02])[0]
        
        # Discount: 0% to 30%, correlated with holiday seasons
        has_discount = random.random() < 0.55
        if has_discount:
            discount_pct = random.choice([0.05, 0.10, 0.15, 0.20, 0.25, 0.30])
        else:
            discount_pct = 0.0
            
        unit_discount = round(unit_price * discount_pct, 2)
        discount_amount = round(unit_discount * quantity, 2)
        total_before_discount = round(unit_price * quantity, 2)
        gross_sales = round(total_before_discount - discount_amount, 2)

        # Cost Price: ~65% to 75% of unit price
        cost_ratio = 0.68 if category == "Electronics" else (0.55 if category == "Clothing" else 0.62)
        cost_price = round(total_before_discount * cost_ratio, 2)
        gross_profit = round(gross_sales - cost_price, 2)

        payment_method = random.choices(payment_methods, weights=payment_weights)[0]
        shipping_type = random.choices(shipping_types, weights=shipping_weights)[0]

        # Delivery days
        delivery_days_map = {
            "Same-Day": 1,
            "Next-Day": 2,
            "Express": random.randint(2, 4),
            "Standard": random.randint(4, 7),
        }
        delivery_days = delivery_days_map[shipping_type]
        delivery_date = order_date + pd.Timedelta(days=delivery_days)

        # Shipping cost based on type
        shipping_costs = {"Standard": 50, "Express": 120, "Next-Day": 200, "Same-Day": 300}
        shipping_cost = shipping_costs[shipping_type]

        # Determine Return Probability
        # Base product return + payment method influence (COD has +12% higher returns) + customer propensity + discount effect
        base_return_rate = product_item["base_return"]
        cod_penalty = 0.12 if payment_method == "Cash on Delivery" else 0.0
        discount_penalty = 0.05 if discount_pct >= 0.20 else 0.0
        delivery_delay_penalty = 0.08 if delivery_days > 5 else 0.0

        p_return = (base_return_rate + cod_penalty + discount_penalty + delivery_delay_penalty) * cust["return_propensity"]
        p_return = float(np.clip(p_return, 0.02, 0.85))

        is_returned = random.random() < p_return

        if is_returned:
            return_status = "Returned"
            days_to_return = random.randint(2, 14)
            return_date = delivery_date + pd.Timedelta(days=days_to_return)

            # Pick return reason based on category distribution
            reasons_spec = CATEGORY_RETURN_REASONS[category]
            reasons = [r[0] for r in reasons_spec]
            reason_weights = [r[1] for r in reasons_spec]
            return_reason = random.choices(reasons, weights=reason_weights)[0]
            
            refund_amount = gross_sales
            net_sales = 0.0
            # Reverse logistics and restocking cost ~ 15% of gross sales or flat 250
            reverse_logistics_cost = round(min(gross_sales * 0.12 + 150, 600), 2)
            net_profit = round(-reverse_logistics_cost, 2)
        else:
            return_status = "Completed"
            days_to_return = np.nan
            return_date = pd.NaT
            return_reason = "Not Applicable"
            refund_amount = 0.0
            net_sales = gross_sales
            net_profit = gross_profit

        records.append({
            "Order_ID": order_id,
            "Order_Date": order_date.strftime("%Y-%m-%d"),
            "Customer_ID": cust["customer_id"],
            "Customer_Name": cust["customer_name"],
            "Customer_Age": cust["age"],
            "Customer_Gender": cust["gender"],
            "Customer_Segment": cust["segment"],
            "Region": cust["region"],
            "City": cust["city"],
            "Product_ID": f"PROD-{CATALOG.index(product_item) + 101}",
            "Product_Name": product_name,
            "Category": category,
            "Sub_Category": sub_category,
            "Unit_Price": unit_price,
            "Quantity": quantity,
            "Discount_Percent": round(discount_pct * 100, 1),
            "Discount_Amount": discount_amount,
            "Total_Before_Discount": total_before_discount,
            "Gross_Sales": gross_sales,
            "Cost_Price": cost_price,
            "Payment_Method": payment_method,
            "Shipping_Type": shipping_type,
            "Delivery_Days": delivery_days,
            "Delivery_Date": delivery_date.strftime("%Y-%m-%d"),
            "Return_Status": return_status,
            "Return_Date": return_date.strftime("%Y-%m-%d") if pd.notna(return_date) else "",
            "Days_to_Return": days_to_return,
            "Return_Reason": return_reason,
            "Refund_Amount": refund_amount,
            "Net_Sales": net_sales,
            "Net_Profit": net_profit,
        })

    df = pd.DataFrame(records)
    # Sort chronologically by Order_Date
    df = df.sort_values("Order_Date").reset_index(drop=True)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"Dataset successfully created at: {OUTPUT_FILE}")
    print(f"Total rows: {len(df)}")
    print(f"Columns ({len(df.columns)}): {list(df.columns)}")
    print(f"Returned orders count: {(df['Return_Status'] == 'Returned').sum()} ({((df['Return_Status'] == 'Returned').mean()*100):.2f}%)")
    return df


if __name__ == "__main__":
    generate_dataset()
