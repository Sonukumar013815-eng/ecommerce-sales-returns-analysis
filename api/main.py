"""
FastAPI Backend — E-Commerce Analytics API
==========================================
Provides REST endpoints for sales KPIs, monthly trends,
category performance, return analysis, customer RFM,
and ML return prediction.

Run with: uvicorn api.main:app --reload --port 8000
"""

import json
import sys
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from analysis import (
    analyze_customer_purchasing_behaviour,
    analyze_product_performance,
    analyze_return_behaviour,
    analyze_sales_performance,
    calculate_sales_kpis,
    clean_and_load_data,
)

app = FastAPI(
    title="E-Commerce Analytics API",
    description="Business intelligence backend for sales, returns, and customer analytics.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Allow Streamlit frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------- Global State ---------------
_df: Optional[pd.DataFrame] = None
_metadata: dict = {}


def get_df() -> pd.DataFrame:
    global _df, _metadata
    if _df is None:
        _df, _metadata = clean_and_load_data()
    return _df


def _df_filtered(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category: Optional[str] = None,
    region: Optional[str] = None,
    payment_method: Optional[str] = None,
    customer_segment: Optional[str] = None,
) -> pd.DataFrame:
    df = get_df().copy()
    if start_date:
        df = df[df["order_date"] >= pd.Timestamp(start_date)]
    if end_date:
        df = df[df["order_date"] <= pd.Timestamp(end_date)]
    if category:
        df = df[df["category"] == category]
    if region:
        df = df[df["region"] == region]
    if payment_method:
        df = df[df["payment_method"] == payment_method]
    if customer_segment:
        df = df[df["customer_segment"] == customer_segment]
    return df


def _safe_json(obj):
    """Convert numpy/pandas types to JSON-serializable Python types."""
    if isinstance(obj, dict):
        return {k: _safe_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_safe_json(i) for i in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.ndarray,)):
        return obj.tolist()
    if isinstance(obj, pd.Timestamp):
        return str(obj)
    if pd.isna(obj) if not isinstance(obj, (list, dict, pd.DataFrame, pd.Series)) else False:
        return None
    return obj


# --------------- Pydantic Schemas ---------------

class PredictRequest(BaseModel):
    category: str = Field("Electronics", example="Electronics")
    sub_category: str = Field("Mobiles", example="Mobiles")
    payment_method: str = Field("Cash on Delivery", example="Cash on Delivery")
    shipping_type: str = Field("Standard", example="Standard")
    customer_segment: str = Field("Consumer", example="Consumer")
    region: str = Field("North", example="North")
    discount_percent: float = Field(10.0, ge=0, le=100)
    unit_price: float = Field(5000.0, ge=0)
    quantity: int = Field(1, ge=1)
    delivery_days: float = Field(5.0, ge=0)
    customer_age: float = Field(30.0, ge=10, le=100)


# --------------- Routes ---------------

@app.get("/")
def root():
    return {"message": "E-Commerce Analytics API v2.0", "docs": "/docs"}


@app.get("/api/health")
def health():
    df = get_df()
    return {"status": "ok", "rows": len(df), "metadata": _metadata}


@app.get("/api/kpis")
def get_kpis(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
):
    """Return high-level sales and return KPIs."""
    try:
        df = _df_filtered(start_date, end_date, category, region)
        kpis = calculate_sales_kpis(df)
        return _safe_json(kpis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sales/monthly")
def get_monthly_sales(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
):
    """Monthly sales trend with gross, net, refunds, and return rate."""
    try:
        df = _df_filtered(start_date, end_date, category, region)
        sales = analyze_sales_performance(df)
        monthly = sales["monthly_trend"].to_dict(orient="records")
        return _safe_json(monthly)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sales/categories")
def get_category_sales(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
):
    """Category-level sales performance."""
    try:
        df = _df_filtered(start_date, end_date, region=region)
        sales = analyze_sales_performance(df)
        categories = sales["category_performance"].to_dict(orient="records")
        return _safe_json(categories)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sales/regions")
def get_region_sales(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
):
    """Regional sales performance."""
    try:
        df = _df_filtered(start_date, end_date, category=category)
        sales = analyze_sales_performance(df)
        regions = sales["regional_performance"].to_dict(orient="records")
        return _safe_json(regions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/returns/reasons")
def get_return_reasons(
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
):
    """Return reasons breakdown (overall and by category)."""
    try:
        df = _df_filtered(category=category, region=region)
        ret = analyze_return_behaviour(df)
        return _safe_json({
            "reasons_overall": ret["reasons_overall"].to_dict(orient="records"),
            "reasons_by_category": ret["reasons_by_category"].to_dict(orient="records"),
            "payment_returns": ret["payment_returns"].to_dict(orient="records"),
            "shipping_returns": ret["shipping_returns"].to_dict(orient="records"),
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/customers/rfm")
def get_rfm(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    """Customer RFM segmentation stats."""
    try:
        df = _df_filtered(start_date, end_date)
        cust = analyze_customer_purchasing_behaviour(df)
        return _safe_json({
            "rfm_segment_stats": cust["rfm_segment_stats"].to_dict(orient="records"),
            "total_unique_customers": cust["total_unique_customers"],
            "repeat_rate_pct": cust["repeat_rate_pct"],
            "serial_returners_count": cust["serial_returners_count"],
            "serial_returners_refund_loss": cust["serial_returners_refund_loss"],
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/products/top")
def get_top_products(limit: int = Query(15, ge=1, le=100)):
    """Top products by net realized sales."""
    try:
        df = get_df()
        prod = analyze_product_performance(df, limit=limit)
        top = prod["top_by_net_sales"].to_dict(orient="records")
        return _safe_json(top)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/products/high-return")
def get_high_return_products(limit: int = Query(15, ge=1, le=100)):
    """Products with the highest return rates (min 20 orders)."""
    try:
        df = get_df()
        prod = analyze_product_performance(df, limit=limit)
        high = prod["highest_returns"].to_dict(orient="records")
        return _safe_json(high)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/filters/options")
def get_filter_options():
    """Return all available filter option values for the dashboard UI."""
    try:
        df = get_df()
        return {
            "categories": sorted(df["category"].dropna().unique().tolist()),
            "regions": sorted(df["region"].dropna().unique().tolist()),
            "payment_methods": sorted(df["payment_method"].dropna().unique().tolist()),
            "customer_segments": sorted(df["customer_segment"].dropna().unique().tolist()),
            "sub_categories": sorted(df["sub_category"].dropna().unique().tolist()),
            "shipping_types": sorted(df["shipping_type"].dropna().unique().tolist()),
            "date_min": str(df["order_date"].min().date()),
            "date_max": str(df["order_date"].max().date()),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/predict/return")
def predict_return(req: PredictRequest):
    """
    ML endpoint: Predict whether an order is likely to be returned.
    Returns probability and risk label.
    """
    try:
        from ml.train_model import predict_single_order

        result = predict_single_order(
            category=req.category,
            sub_category=req.sub_category,
            payment_method=req.payment_method,
            shipping_type=req.shipping_type,
            customer_segment=req.customer_segment,
            region=req.region,
            discount_percent=req.discount_percent,
            unit_price=req.unit_price,
            quantity=req.quantity,
            delivery_days=req.delivery_days,
            customer_age=req.customer_age,
        )
        return _safe_json(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
