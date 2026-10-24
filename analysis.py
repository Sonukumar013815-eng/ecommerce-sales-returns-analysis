"""
E-Commerce Sales, Returns, and Customer Analysis Engine
======================================================
Robust data cleaning, validation, transformation, KPI calculations,
customer purchasing behaviour (RFM), return patterns, anomaly detection,
and automated reporting.
"""

from pathlib import Path
import json
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Directory definitions
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def find_dataset():
    """Locate the best dataset file in the data folder."""
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Prefer ecommerce_orders_and_returns.csv if present
    preferred = DATA_DIR / "ecommerce_orders_and_returns.csv"
    if preferred.exists():
        return preferred

    candidates = (
        list(DATA_DIR.glob("*.csv"))
        + list(DATA_DIR.glob("*.xlsx"))
        + list(DATA_DIR.glob("*.xls"))
    )

    if not candidates:
        raise FileNotFoundError(
            f"No dataset found in {DATA_DIR}. "
            "Please add your e-commerce orders and returns CSV or Excel file."
        )

    return candidates[0]


def clean_and_load_data(file_path=None):
    """
    Load raw dataset, standardize column names, validate types,
    handle missing values, remove duplicates, and derive analytical measures.
    """
    path = Path(file_path) if file_path else find_dataset()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    # Read data
    if path.suffix.lower() == ".csv":
        try:
            df = pd.read_csv(path, encoding="utf-8-sig")
        except UnicodeDecodeError:
            df = pd.read_csv(path, encoding="latin1")
    elif path.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported format: {path.suffix}")

    # Standardize column headers (lower, strip, replace spaces/dashes with underscores)
    df.columns = [str(col).strip().replace(" ", "_").replace("-", "_") for col in df.columns]
    normalized_cols = {col.lower(): col for col in df.columns}

    # Alias mapping for flexible schema support (Kaggle datasets / Superstore variations)
    aliases = {
        "order_id": ["order_id", "orderid", "id", "transaction_id", "order_number"],
        "order_date": ["order_date", "date", "purchase_date", "orderdate"],
        "customer_id": ["customer_id", "customerid", "user_id", "userid", "client_id"],
        "customer_name": ["customer_name", "customername", "user_name", "name", "client_name"],
        "customer_age": ["customer_age", "age", "user_age"],
        "customer_gender": ["customer_gender", "gender", "user_gender", "sex"],
        "customer_segment": ["customer_segment", "segment", "customer_type", "user_type"],
        "region": ["region", "sales_region", "zone", "state", "user_location"],
        "city": ["city", "town", "location"],
        "product_id": ["product_id", "productid", "item_id", "sku"],
        "product_name": ["product_name", "product", "item_name", "product_title"],
        "category": ["category", "product_category", "department"],
        "sub_category": ["sub_category", "subcategory", "product_sub_category"],
        "unit_price": ["unit_price", "price", "product_price", "item_price"],
        "quantity": ["quantity", "qty", "order_quantity", "units"],
        "discount_percent": ["discount_percent", "discount_pct", "discount_rate"],
        "discount_amount": ["discount_amount", "discount", "discount_value"],
        "gross_sales": ["gross_sales", "sales", "revenue", "amount", "total_sales"],
        "payment_method": ["payment_method", "payment", "payment_mode", "payment_type"],
        "shipping_type": ["shipping_type", "shipping", "shipping_method", "delivery_type"],
        "delivery_days": ["delivery_days", "shipping_days", "transit_days"],
        "return_status": ["return_status", "returned", "is_returned", "order_status"],
        "return_date": ["return_date", "returndate"],
        "days_to_return": ["days_to_return", "return_days", "days_until_return"],
        "return_reason": ["return_reason", "reason_for_return", "reason"],
        "refund_amount": ["refund_amount", "refund", "returned_amount"],
        "net_sales": ["net_sales", "realized_sales", "final_sales"],
        "net_profit": ["net_profit", "profit", "margin", "operating_profit"],
    }

    rename_dict = {}
    for standard_col, options in aliases.items():
        for opt in options:
            if opt in normalized_cols:
                rename_dict[normalized_cols[opt]] = standard_col
                break

    df = df.rename(columns=rename_dict)

    # 1. Deduplication
    initial_rows = len(df)
    if "order_id" in df.columns:
        df = df.drop_duplicates(subset=["order_id"])
    else:
        df = df.drop_duplicates()
    dropped_dupes = initial_rows - len(df)

    # 2. Date Parsing & Validation
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    else:
        df["order_date"] = pd.Timestamp.now()

    if "return_date" in df.columns:
        df["return_date"] = pd.to_datetime(df["return_date"], errors="coerce")
    else:
        df["return_date"] = pd.NaT

    # 3. Numeric conversions & defaults
    numeric_cols = [
        "unit_price", "quantity", "discount_percent", "discount_amount",
        "gross_sales", "delivery_days", "days_to_return", "refund_amount",
        "net_sales", "net_profit", "customer_age"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "quantity" not in df.columns:
        df["quantity"] = 1
    df["quantity"] = df["quantity"].fillna(1).clip(lower=1)

    if "unit_price" not in df.columns:
        if "gross_sales" in df.columns:
            df["unit_price"] = df["gross_sales"] / df["quantity"]
        else:
            df["unit_price"] = 100.0
    df["unit_price"] = df["unit_price"].fillna(0.0).clip(lower=0.0)

    if "discount_percent" not in df.columns:
        df["discount_percent"] = 0.0
    df["discount_percent"] = df["discount_percent"].fillna(0.0)

    if "gross_sales" not in df.columns:
        df["gross_sales"] = df["unit_price"] * df["quantity"] * (1 - df["discount_percent"] / 100)
    df["gross_sales"] = df["gross_sales"].fillna(0.0).clip(lower=0.0)

    # 4. Standardize Return Status
    if "return_status" in df.columns:
        df["return_status"] = (
            df["return_status"]
            .astype(str)
            .str.strip()
            .replace({"1": "Returned", "1.0": "Returned", "True": "Returned", "true": "Returned", "yes": "Returned", "Yes": "Returned"})
        )
        df["is_returned"] = df["return_status"].str.lower().isin(["returned", "refunded", "cancelled", "true"])
        df["return_status"] = np.where(df["is_returned"], "Returned", "Completed")
    elif "is_returned" in df.columns:
        df["is_returned"] = df["is_returned"].astype(bool)
        df["return_status"] = np.where(df["is_returned"], "Returned", "Completed")
    else:
        df["is_returned"] = False
        df["return_status"] = "Completed"

    # 5. Missing Categorical Defaults
    categorical_defaults = {
        "customer_id": "CUST-UNKNOWN",
        "customer_name": "Anonymous Customer",
        "customer_segment": "Consumer",
        "customer_gender": "Unspecified",
        "region": "General",
        "city": "Unknown City",
        "product_id": "PROD-GEN",
        "product_name": "General Item",
        "category": "General Merchandise",
        "sub_category": "Miscellaneous",
        "payment_method": "Prepaid / Unknown",
        "shipping_type": "Standard",
        "return_reason": "Not Applicable",
    }
    for col, default_val in categorical_defaults.items():
        if col not in df.columns:
            df[col] = default_val
        df[col] = df[col].fillna(default_val).astype(str).str.strip()

    # Align return reason with return status
    df.loc[~df["is_returned"], "return_reason"] = "Not Applicable"
    df.loc[df["is_returned"] & (df["return_reason"].isin(["Not Applicable", "", "nan", "None"])), "return_reason"] = "Unspecified Reason"

    # 6. Derived Measures
    if "refund_amount" not in df.columns or df["refund_amount"].isna().all():
        df["refund_amount"] = np.where(df["is_returned"], df["gross_sales"], 0.0)

    if "net_sales" not in df.columns or df["net_sales"].isna().all():
        df["net_sales"] = np.where(df["is_returned"], 0.0, df["gross_sales"])

    if "net_profit" not in df.columns or df["net_profit"].isna().all():
        # Estimated cost ~65% of gross sales, return processing cost ~15%
        df["net_profit"] = np.where(
            df["is_returned"],
            - (df["gross_sales"] * 0.15 + 100),
            df["gross_sales"] * 0.35
        )

    # Date-based derived features
    df["order_year"] = df["order_date"].dt.year
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
    df["order_year_month"] = df["order_date"].dt.strftime("%Y-%m")
    df["order_quarter"] = df["order_date"].dt.to_period("Q").astype(str)
    df["order_day_name"] = df["order_date"].dt.day_name()

    # Derived tiers
    df["discount_tier"] = pd.cut(
        df["discount_percent"],
        bins=[-1, 0, 10, 20, 100],
        labels=["No Discount (0%)", "Low (1-10%)", "Medium (11-20%)", "High (>20%)"]
    )
    df["price_tier"] = pd.cut(
        df["unit_price"],
        bins=[-1, 1000, 5000, 20000, np.inf],
        labels=["Budget (<Rs. 1,000)", "Mid-Range (Rs. 1,000-Rs. 5,000)", "Premium (Rs. 5,000-Rs. 20,000)", "Luxury (>Rs. 20,000)"]
    )

    metadata = {
        "file_path": str(path),
        "total_records": len(df),
        "dropped_duplicates": dropped_dupes,
        "date_min": str(df["order_date"].min().date()) if not df["order_date"].isna().all() else None,
        "date_max": str(df["order_date"].max().date()) if not df["order_date"].isna().all() else None,
    }

    return df, metadata


def calculate_sales_kpis(df):
    """Calculate overall high-level business and financial KPIs."""
    gross_sales = float(df["gross_sales"].sum())
    net_sales = float(df["net_sales"].sum())
    total_refunds = float(df["refund_amount"].sum())
    total_orders = int(df["order_id"].nunique()) if "order_id" in df.columns else len(df)
    total_units = int(df["quantity"].sum())
    total_customers = int(df["customer_id"].nunique()) if "customer_id" in df.columns else total_orders

    returned_orders = int(df["is_returned"].sum())
    return_rate_orders = (returned_orders / total_orders * 100) if total_orders > 0 else 0.0
    return_rate_sales = (total_refunds / gross_sales * 100) if gross_sales > 0 else 0.0
    realization_rate = (net_sales / gross_sales * 100) if gross_sales > 0 else 0.0

    aov_gross = (gross_sales / total_orders) if total_orders > 0 else 0.0
    aov_net = (net_sales / (total_orders - returned_orders)) if (total_orders - returned_orders) > 0 else 0.0

    avg_discount = float(df["discount_percent"].mean())
    avg_delivery_days = float(df["delivery_days"].dropna().mean()) if "delivery_days" in df.columns else 0.0
    avg_days_to_return = float(df[df["is_returned"]]["days_to_return"].dropna().mean())

    total_net_profit = float(df["net_profit"].sum())
    profit_margin = (total_net_profit / net_sales * 100) if net_sales > 0 else 0.0

    return {
        "gross_sales": gross_sales,
        "net_sales": net_sales,
        "total_refunds": total_refunds,
        "net_revenue_realization_rate": realization_rate,
        "total_orders": total_orders,
        "returned_orders": returned_orders,
        "order_return_rate_pct": return_rate_orders,
        "sales_return_rate_pct": return_rate_sales,
        "total_units_sold": total_units,
        "total_customers": total_customers,
        "aov_gross": aov_gross,
        "aov_net": aov_net,
        "avg_discount_pct": avg_discount,
        "avg_delivery_days": avg_delivery_days,
        "avg_days_to_return": avg_days_to_return,
        "total_net_profit": total_net_profit,
        "net_profit_margin_pct": profit_margin,
    }


def analyze_sales_performance(df):
    """Analyze monthly trends, regional breakdown, and category sales."""
    # Monthly sales trend
    monthly = (
        df.groupby("order_year_month", dropna=False)
        .agg(
            gross_sales=("gross_sales", "sum"),
            net_sales=("net_sales", "sum"),
            refunds=("refund_amount", "sum"),
            orders=("order_id", "nunique"),
            returns=("is_returned", "sum"),
        )
        .reset_index()
        .sort_values("order_year_month")
    )
    monthly["return_rate_pct"] = (monthly["returns"] / monthly["orders"] * 100).round(2)
    monthly["realization_rate_pct"] = (monthly["net_sales"] / monthly["gross_sales"] * 100).round(2)

    # Category performance
    category = (
        df.groupby("category", dropna=False)
        .agg(
            gross_sales=("gross_sales", "sum"),
            net_sales=("net_sales", "sum"),
            refunds=("refund_amount", "sum"),
            units_sold=("quantity", "sum"),
            orders=("order_id", "nunique"),
            returns=("is_returned", "sum"),
        )
        .reset_index()
    )
    category["return_rate_pct"] = (category["returns"] / category["orders"] * 100).round(2)
    category["revenue_loss_pct"] = (category["refunds"] / category["gross_sales"] * 100).round(2)
    category = category.sort_values("gross_sales", ascending=False)

    # Regional performance
    region = (
        df.groupby("region", dropna=False)
        .agg(
            gross_sales=("gross_sales", "sum"),
            net_sales=("net_sales", "sum"),
            orders=("order_id", "nunique"),
            returns=("is_returned", "sum"),
        )
        .reset_index()
    )
    region["return_rate_pct"] = (region["returns"] / region["orders"] * 100).round(2)
    region = region.sort_values("gross_sales", ascending=False)

    return {
        "monthly_trend": monthly,
        "category_performance": category,
        "regional_performance": region,
    }


def analyze_customer_purchasing_behaviour(df):
    """
    Analyze customer frequency, RFM segmentation, Repeat Purchase Rate,
    and detect Serial Returners.
    """
    cust_summary = (
        df.groupby(["customer_id", "customer_name", "customer_segment"], dropna=False)
        .agg(
            total_orders=("order_id", "nunique"),
            total_gross_spend=("gross_sales", "sum"),
            total_net_spend=("net_sales", "sum"),
            total_returns=("is_returned", "sum"),
            last_order_date=("order_date", "max"),
            first_order_date=("order_date", "min"),
        )
        .reset_index()
    )

    cust_summary["return_rate_pct"] = (
        cust_summary["total_returns"] / cust_summary["total_orders"] * 100
    ).round(2)

    # Reference date for recency calculation
    max_date = df["order_date"].max()
    cust_summary["recency_days"] = (max_date - cust_summary["last_order_date"]).dt.days

    # Customer purchase frequency metrics
    repeat_customers = cust_summary[cust_summary["total_orders"] > 1]
    repeat_rate_pct = (len(repeat_customers) / len(cust_summary) * 100) if len(cust_summary) > 0 else 0.0

    # Identify Serial Returners (>= 3 orders and >= 50% return rate)
    serial_returners = cust_summary[
        (cust_summary["total_orders"] >= 3) & (cust_summary["return_rate_pct"] >= 50.0)
    ]
    serial_returner_orders = df[df["customer_id"].isin(serial_returners["customer_id"])]

    # RFM Scoring
    # R: 1 (least recent) to 4 (most recent)
    # F: 1 (low frequency) to 4 (high frequency)
    # M: 1 (low spend) to 4 (high spend)
    try:
        cust_summary["r_score"] = pd.qcut(cust_summary["recency_days"], q=4, labels=[4, 3, 2, 1])
        cust_summary["f_score"] = pd.qcut(cust_summary["total_orders"].rank(method="first"), q=4, labels=[1, 2, 3, 4])
        cust_summary["m_score"] = pd.qcut(cust_summary["total_net_spend"].rank(method="first"), q=4, labels=[1, 2, 3, 4])
        
        # Segment label assignment
        def assign_segment(row):
            rfm = int(row["r_score"]) + int(row["f_score"]) + int(row["m_score"])
            if rfm >= 10:
                return "Champions & VIPs"
            elif rfm >= 8:
                return "Loyal Customers"
            elif rfm >= 6:
                return "Potential Loyalists"
            elif rfm >= 4:
                return "At Risk / Promising"
            else:
                return "Hibernating / Inactive"

        cust_summary["rfm_segment"] = cust_summary.apply(assign_segment, axis=1)
    except Exception:
        cust_summary["rfm_segment"] = "Standard Customer"

    # Segment overview
    segment_stats = (
        cust_summary.groupby("rfm_segment")
        .agg(
            customer_count=("customer_id", "count"),
            avg_gross_spend=("total_gross_spend", "mean"),
            avg_return_rate=("return_rate_pct", "mean"),
            total_revenue=("total_net_spend", "sum"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )

    return {
        "customer_summary": cust_summary,
        "repeat_rate_pct": round(repeat_rate_pct, 2),
        "total_unique_customers": len(cust_summary),
        "repeat_customers_count": len(repeat_customers),
        "serial_returners_count": len(serial_returners),
        "serial_returners_refund_loss": float(serial_returner_orders["refund_amount"].sum()),
        "rfm_segment_stats": segment_stats,
    }


def analyze_product_performance(df, limit=15):
    """Analyze best/worst selling products and products with highest return rates."""
    product_stats = (
        df.groupby(["product_id", "product_name", "category", "sub_category"], dropna=False)
        .agg(
            gross_sales=("gross_sales", "sum"),
            net_sales=("net_sales", "sum"),
            refunds=("refund_amount", "sum"),
            units_sold=("quantity", "sum"),
            total_orders=("order_id", "nunique"),
            returns=("is_returned", "sum"),
            avg_price=("unit_price", "mean"),
        )
        .reset_index()
    )

    product_stats["return_rate_pct"] = (
        product_stats["returns"] / product_stats["total_orders"] * 100
    ).round(2)
    product_stats["sales_loss_pct"] = (
        product_stats["refunds"] / product_stats["gross_sales"] * 100
    ).round(2)

    top_by_net_sales = product_stats.sort_values("net_sales", ascending=False).head(limit)
    highest_returns = product_stats[product_stats["total_orders"] >= 20].sort_values("return_rate_pct", ascending=False).head(limit)

    return {
        "all_products": product_stats,
        "top_by_net_sales": top_by_net_sales,
        "highest_returns": highest_returns,
    }


def analyze_return_behaviour(df):
    """Deep-dive into return causes, category return patterns, payment methods, and transit days."""
    returned_df = df[df["is_returned"]].copy()

    # 1. Return reasons overall
    reasons_overall = (
        returned_df["return_reason"]
        .value_counts()
        .reset_index()
    )
    reasons_overall.columns = ["return_reason", "return_count"]
    reasons_overall["pct_of_all_returns"] = (
        reasons_overall["return_count"] / len(returned_df) * 100
    ).round(2)

    # 2. Return reasons by category
    reasons_by_category = (
        returned_df.groupby(["category", "return_reason"])
        .size()
        .reset_index(name="count")
        .sort_values(["category", "count"], ascending=[True, False])
    )

    # 3. Return rate by Payment Method
    payment_returns = (
        df.groupby("payment_method", dropna=False)
        .agg(
            total_orders=("order_id", "nunique"),
            returned_orders=("is_returned", "sum"),
            gross_sales=("gross_sales", "sum"),
            refund_amount=("refund_amount", "sum"),
        )
        .reset_index()
    )
    payment_returns["return_rate_pct"] = (
        payment_returns["returned_orders"] / payment_returns["total_orders"] * 100
    ).round(2)
    payment_returns = payment_returns.sort_values("return_rate_pct", ascending=False)

    # 4. Return rate by Shipping Type
    shipping_returns = (
        df.groupby("shipping_type", dropna=False)
        .agg(
            total_orders=("order_id", "nunique"),
            returned_orders=("is_returned", "sum"),
            avg_delivery_days=("delivery_days", "mean"),
        )
        .reset_index()
    )
    shipping_returns["return_rate_pct"] = (
        shipping_returns["returned_orders"] / shipping_returns["total_orders"] * 100
    ).round(2)
    shipping_returns = shipping_returns.sort_values("return_rate_pct", ascending=False)

    # 5. Return rate by Discount Tier
    discount_returns = (
        df.groupby("discount_tier", observed=False)
        .agg(
            total_orders=("order_id", "nunique"),
            returned_orders=("is_returned", "sum"),
            gross_sales=("gross_sales", "sum"),
        )
        .reset_index()
    )
    discount_returns["return_rate_pct"] = (
        discount_returns["returned_orders"] / discount_returns["total_orders"] * 100
    ).round(2)

    # 6. Days to Return distribution metrics
    days_data = returned_df["days_to_return"].dropna()
    days_stats = {
        "mean_days": float(days_data.mean()) if not days_data.empty else 0.0,
        "median_days": float(days_data.median()) if not days_data.empty else 0.0,
        "min_days": float(days_data.min()) if not days_data.empty else 0.0,
        "max_days": float(days_data.max()) if not days_data.empty else 0.0,
    }

    return {
        "reasons_overall": reasons_overall,
        "reasons_by_category": reasons_by_category,
        "payment_returns": payment_returns,
        "shipping_returns": shipping_returns,
        "discount_returns": discount_returns,
        "days_to_return_stats": days_stats,
    }


def detect_anomalies_and_insights(df):
    """
    Automated discovery of anomalies, disproportionate returns,
    and business takeaways.
    """
    insights = []
    
    kpis = calculate_sales_kpis(df)
    ret_beh = analyze_return_behaviour(df)
    cust_beh = analyze_customer_purchasing_behaviour(df)

    # 1. Overall return rate observation
    overall_ret_rate = kpis["order_return_rate_pct"]
    if overall_ret_rate > 20:
        insights.append({
            "type": "High Overall Returns",
            "level": "Warning",
            "finding": f"Overall order return rate is {overall_ret_rate:.1f}%, resulting in Rs. {kpis['total_refunds']:,.0f} of refunded revenue ({kpis['sales_return_rate_pct']:.1f}% of gross sales).",
            "recommendation": "Review post-order confirmation and fit/quality guidance to reduce return velocity."
        })

    # 2. Category with highest return rate
    cat_stats = df.groupby("category").agg(
        orders=("order_id", "nunique"),
        returns=("is_returned", "sum"),
        refunds=("refund_amount", "sum")
    ).reset_index()
    cat_stats["ret_rate"] = cat_stats["returns"] / cat_stats["orders"] * 100
    top_cat = cat_stats.sort_values("ret_rate", ascending=False).iloc[0]
    
    insights.append({
        "type": "Highest Return Category",
        "level": "Alert",
        "finding": f"'{top_cat['category']}' exhibits the highest return rate at {top_cat['ret_rate']:.1f}% (Refund loss: Rs. {top_cat['refunds']:,.0f}).",
        "recommendation": "Target this category with enhanced visual sizing charts, customer reviews, or pre-shipping inspection."
    })

    # 3. Payment Method: COD vs Prepaid
    pm_stats = ret_beh["payment_returns"]
    cod_row = pm_stats[pm_stats["payment_method"] == "Cash on Delivery"]
    if not cod_row.empty:
        cod_rate = float(cod_row["return_rate_pct"].iloc[0])
        prepaid_rate = float(pm_stats[pm_stats["payment_method"] != "Cash on Delivery"]["return_rate_pct"].mean())
        if cod_rate > prepaid_rate + 5:
            insights.append({
                "type": "Cash on Delivery Return Spike",
                "level": "Critical",
                "finding": f"COD orders experience a {cod_rate:.1f}% return/refusal rate compared to {prepaid_rate:.1f}% for prepaid methods (+{cod_rate - prepaid_rate:.1f}% gap).",
                "recommendation": "Incentivize digital prepayment (UPI/Cards) via 2-5% instant cashback or require OTP verification on COD dispatches."
            })

    # 4. Serial returners insight
    serial_cnt = cust_beh["serial_returners_count"]
    serial_loss = cust_beh["serial_returners_refund_loss"]
    if serial_cnt > 0:
        insights.append({
            "type": "Serial Returners Impact",
            "level": "Notice",
            "finding": f"{serial_cnt} customers were identified as serial returners (>=3 orders and >=50% return rate), generating Rs. {serial_loss:,.0f} in return refunds.",
            "recommendation": "Implement targeted return fees or require manual review on high-frequency return profiles."
        })

    # 5. Primary return reason
    top_reason = ret_beh["reasons_overall"].iloc[0]
    insights.append({
        "type": "Dominant Return Driver",
        "level": "Info",
        "finding": f"The top stated return reason is '{top_reason['return_reason']}', accounting for {top_reason['pct_of_all_returns']:.1f}% of all returns ({top_reason['return_count']} orders).",
        "recommendation": "Audit product listing descriptions, dimensional accuracy, and QA checks for this failure mode."
    })

    return insights


def generate_static_charts(df):
    """Generate and export high-resolution publication-quality summary charts."""
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    
    # 1. Monthly Gross vs Net Sales Chart
    monthly_data = (
        df.groupby("order_year_month")
        .agg(gross_sales=("gross_sales", "sum"), net_sales=("net_sales", "sum"))
        .reset_index()
    )
    
    fig, ax1 = plt.subplots(figsize=(11, 5))
    x = np.arange(len(monthly_data))
    width = 0.35

    ax1.bar(x - width/2, monthly_data["gross_sales"] / 1000, width, label="Gross Sales (Rs. k)", color="#3b82f6", alpha=0.85)
    ax1.bar(x + width/2, monthly_data["net_sales"] / 1000, width, label="Net Realized Sales (Rs. k)", color="#10b981", alpha=0.85)
    
    ax1.set_title("E-Commerce Monthly Sales Performance: Gross vs Net Realized Revenue", fontsize=13, fontweight="bold", pad=12)
    ax1.set_xlabel("Month", fontweight="bold")
    ax1.set_ylabel("Revenue (Rs. Thousands)", fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(monthly_data["order_year_month"], rotation=45, ha="right")
    ax1.legend(loc="upper left")
    plt.tight_layout()
    chart1_path = OUTPUT_DIR / "monthly_sales_comparison.png"
    plt.savefig(chart1_path, dpi=200)
    plt.close()

    # 2. Return Rate by Category Chart
    cat_summary = (
        df.groupby("category")
        .agg(orders=("order_id", "nunique"), returns=("is_returned", "sum"))
        .reset_index()
    )
    cat_summary["return_rate"] = cat_summary["returns"] / cat_summary["orders"] * 100
    cat_summary = cat_summary.sort_values("return_rate", ascending=True)

    fig, ax2 = plt.subplots(figsize=(9, 4.5))
    colors = ["#ef4444" if r > 22 else "#f59e0b" if r > 15 else "#10b981" for r in cat_summary["return_rate"]]
    bars = ax2.barh(cat_summary["category"], cat_summary["return_rate"], color=colors, alpha=0.85)
    ax2.set_title("Product Return Rate by Category (%)", fontsize=13, fontweight="bold", pad=12)
    ax2.set_xlabel("Return Rate (%)", fontweight="bold")
    ax2.axvline(x=20, color="gray", linestyle="--", alpha=0.7, label="20% Threshold")
    
    for bar in bars:
        w = bar.get_width()
        ax2.text(w + 0.5, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", va="center", fontweight="bold", fontsize=10)

    ax2.legend()
    plt.tight_layout()
    chart2_path = OUTPUT_DIR / "category_return_rates.png"
    plt.savefig(chart2_path, dpi=200)
    plt.close()

    return [chart1_path, chart2_path]


def generate_executive_report(df, metadata):
    """Generate an extensive, formal markdown executive report with all findings."""
    kpis = calculate_sales_kpis(df)
    sales_perf = analyze_sales_performance(df)
    cust_perf = analyze_customer_purchasing_behaviour(df)
    prod_perf = analyze_product_performance(df)
    ret_perf = analyze_return_behaviour(df)
    insights = detect_anomalies_and_insights(df)

    report_path = OUTPUT_DIR / "Executive_Business_Report.md"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Executive Business Report: E-Commerce Sales, Returns & Customer Analysis\n\n")
        f.write(f"**Generated Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Dataset Source:** `{metadata['file_path']}` | **Analyzed Records:** {metadata['total_records']:,}\n")
        f.write(f"**Date Range:** {metadata['date_min']} to {metadata['date_max']}\n\n")

        f.write("---\n\n")
        f.write("## 1. Executive Summary & Core KPIs\n\n")
        f.write(f"- **Gross Sales (Total Invoiced):** Rs. {kpis['gross_sales']:,.2f}\n")
        f.write(f"- **Net Sales (Realized):** Rs. {kpis['net_sales']:,.2f}\n")
        f.write(f"- **Revenue Realization Rate:** {kpis['net_revenue_realization_rate']:.2f}% (Loss to returns: {100 - kpis['net_revenue_realization_rate']:.2f}%)\n")
        f.write(f"- **Total Refund Loss:** Rs. {kpis['total_refunds']:,.2f}\n")
        f.write(f"- **Total Orders Processed:** {kpis['total_orders']:,}\n")
        f.write(f"- **Total Returned Orders:** {kpis['returned_orders']:,} ({kpis['order_return_rate_pct']:.2f}% Order Return Rate)\n")
        f.write(f"- **Total Units Sold:** {kpis['total_units_sold']:,}\n")
        f.write(f"- **Active Customer Base:** {kpis['total_customers']:,}\n")
        f.write(f"- **Average Order Value (Gross):** Rs. {kpis['aov_gross']:,.2f}\n")
        f.write(f"- **Average Days to Return:** {kpis['avg_days_to_return']:.1f} days\n")
        f.write(f"- **Estimated Net Profit:** Rs. {kpis['total_net_profit']:,.2f} ({kpis['net_profit_margin_pct']:.1f}% Margin)\n\n")

        f.write("---\n\n")
        f.write("## 2. Strategic Insights & Anomalies Detected\n\n")
        for i, ins in enumerate(insights, 1):
            f.write(f"### {i}. [{ins['level']}] {ins['type']}\n")
            f.write(f"- **Finding:** {ins['finding']}\n")
            f.write(f"- **Recommended Business Action:** {ins['recommendation']}\n\n")

        f.write("---\n\n")
        f.write("## 3. Product Category & Sales Breakdown\n\n")
        f.write("| Category | Gross Sales | Net Sales | Refund Loss | Orders | Returns | Return Rate % |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for _, row in sales_perf["category_performance"].iterrows():
            f.write(f"| {row['category']} | Rs. {row['gross_sales']:,.0f} | Rs. {row['net_sales']:,.0f} | Rs. {row['refunds']:,.0f} | {row['orders']:,} | {row['returns']:,} | **{row['return_rate_pct']:.1f}%** |\n")

        f.write("\n---\n\n")
        f.write("## 4. Customer Purchasing Behaviour & RFM Segmentation\n\n")
        f.write(f"- **Unique Customers:** {cust_perf['total_unique_customers']:,}\n")
        f.write(f"- **Repeat Purchase Rate:** {cust_perf['repeat_rate_pct']}%\n")
        f.write(f"- **Identified Serial Returners:** {cust_perf['serial_returners_count']} accounts (Accountable for Rs. {cust_perf['serial_returners_refund_loss']:,.0f} in refunded gross sales)\n\n")
        f.write("| RFM Customer Segment | Customer Count | Avg Gross Spend | Avg Return Rate % | Net Revenue Contribution |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        for _, row in cust_perf["rfm_segment_stats"].iterrows():
            f.write(f"| {row['rfm_segment']} | {row['customer_count']:,} | Rs. {row['avg_gross_spend']:,.0f} | {row['avg_return_rate']:.1f}% | Rs. {row['total_revenue']:,.0f} |\n")

        f.write("\n---\n\n")
        f.write("## 5. Return Root Cause Breakdown\n\n")
        f.write("| Stated Return Reason | Number of Returns | Share of Returns % |\n")
        f.write("| :--- | :--- | :--- |\n")
        for _, row in ret_perf["reasons_overall"].iterrows():
            f.write(f"| {row['return_reason']} | {row['return_count']:,} | {row['pct_of_all_returns']:.1f}% |\n")

        f.write("\n---\n\n")
        f.write("## 6. Payment & Shipping Method Dynamics\n\n")
        f.write("### Payment Method Return Propensity\n\n")
        f.write("| Payment Method | Orders | Returned Orders | Return Rate % | Total Refunds |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        for _, row in ret_perf["payment_returns"].iterrows():
            f.write(f"| {row['payment_method']} | {row['total_orders']:,} | {row['returned_orders']:,} | **{row['return_rate_pct']:.1f}%** | Rs. {row['refund_amount']:,.0f} |\n")

        f.write("\n*End of Executive Business Report.*\n")

    return report_path


def run_full_pipeline(file_path=None):
    """Execute complete end-to-end data processing, analytics, and exports."""
    print("=" * 60)
    print("Starting E-Commerce Analytics Engine Pipeline...")
    print("=" * 60)

    # 1. Clean & Load
    df, metadata = clean_and_load_data(file_path)
    print(f"[1/6] Data loaded successfully: {metadata['total_records']:,} records from {metadata['file_path']}")
    if metadata['dropped_duplicates'] > 0:
        print(f"      Deduplication: removed {metadata['dropped_duplicates']} duplicate records.")

    # 2. Compute KPIs
    kpis = calculate_sales_kpis(df)
    print(f"[2/6] Core KPIs calculated:")
    print(f"      Gross Sales: Rs. {kpis['gross_sales']:,.2f}")
    print(f"      Net Sales:   Rs. {kpis['net_sales']:,.2f}")
    print(f"      Return Rate: {kpis['order_return_rate_pct']:.2f}% ({kpis['returned_orders']:,} returned orders)")

    # 3. Analyze Sales, Customers, Products, Returns
    sales_analysis = analyze_sales_performance(df)
    customer_analysis = analyze_customer_purchasing_behaviour(df)
    product_analysis = analyze_product_performance(df)
    return_analysis = analyze_return_behaviour(df)
    print(f"[3/6] Completed dimensional breakdowns across sales, customers, products, and returns.")

    # 4. Anomaly Detection
    insights = detect_anomalies_and_insights(df)
    print(f"[4/6] Anomaly detection completed: {len(insights)} high-priority observations flagged.")

    # 5. Export Summary CSVs
    sales_analysis["monthly_trend"].to_csv(OUTPUT_DIR / "monthly_sales_trend.csv", index=False)
    sales_analysis["category_performance"].to_csv(OUTPUT_DIR / "category_performance.csv", index=False)
    product_analysis["top_by_net_sales"].to_csv(OUTPUT_DIR / "top_products_net_sales.csv", index=False)
    product_analysis["highest_returns"].to_csv(OUTPUT_DIR / "highest_return_products.csv", index=False)
    return_analysis["reasons_overall"].to_csv(OUTPUT_DIR / "return_reasons_summary.csv", index=False)
    return_analysis["payment_returns"].to_csv(OUTPUT_DIR / "returns_by_payment_method.csv", index=False)
    customer_analysis["rfm_segment_stats"].to_csv(OUTPUT_DIR / "customer_rfm_segments.csv", index=False)
    
    with open(OUTPUT_DIR / "insights.json", "w", encoding="utf-8") as f:
        json.dump(insights, f, indent=2)

    print(f"[5/6] Exported 7 CSV summary tables and JSON insights to '{OUTPUT_DIR}'")

    # 6. Static Charts & Executive Report
    chart_paths = generate_static_charts(df)
    report_path = generate_executive_report(df, metadata)
    print(f"[6/6] Saved static charts and generated executive report:")
    print(f"      Report: {report_path}")
    for cp in chart_paths:
        print(f"      Chart:  {cp}")

    print("=" * 60)
    print("Pipeline Execution Complete!")
    print("=" * 60)
    return df, kpis, insights


if __name__ == "__main__":
    run_full_pipeline()
