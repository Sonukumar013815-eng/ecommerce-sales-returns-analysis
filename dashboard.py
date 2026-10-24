"""
E-Commerce Sales, Returns, and Customer Analysis Dashboard
=========================================================
Interactive business intelligence dashboard built with Streamlit and Plotly.
Provides executive KPIs, sales trends, customer purchasing behaviour (RFM),
product/category performance, return root cause analysis, and anomaly alerts.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from analysis import (
    clean_and_load_data,
    calculate_sales_kpis,
    analyze_sales_performance,
    analyze_customer_purchasing_behaviour,
    analyze_product_performance,
    analyze_return_behaviour,
    detect_anomalies_and_insights,
)

BASE_DIR = Path(__file__).resolve().parent

# Page setup
st.set_page_config(
    page_title="E-Commerce Sales, Returns & Customer Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 14px 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-title {
        font-size: 0.82rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 1.55rem;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-subtitle {
        font-size: 0.78rem;
        color: #94a3b8;
    }
    .badge-alert {
        background-color: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    .badge-warning {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    .badge-info {
        background-color: #f0fdf4;
        border-left: 4px solid #10b981;
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_cleaned_data():
    """Load and clean dataset with caching for rapid interaction."""
    df, meta = clean_and_load_data()
    return df, meta


try:
    raw_df, metadata = get_cleaned_data()
except Exception as exc:
    st.error("Error loading the e-commerce dataset.")
    st.info("Ensure `ecommerce_orders_and_returns.csv` exists in the `data/` folder.")
    st.exception(exc)
    st.stop()


# -------------------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=64)
    st.title("Filters & Controls")
    st.caption(f"Source: `{Path(metadata['file_path']).name}` ({metadata['total_records']:,} rows)")

    # Date Range Filter
    valid_dates = raw_df["order_date"].dropna()
    if not valid_dates.empty:
        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()
        selected_date_range = st.date_input(
            "📅 Order Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )
    else:
        selected_date_range = None

    # Category Filter
    all_categories = sorted(raw_df["category"].dropna().unique().tolist())
    selected_categories = st.multiselect("🏷️ Category", all_categories, default=all_categories)

    # Region Filter
    all_regions = sorted(raw_df["region"].dropna().unique().tolist())
    selected_regions = st.multiselect("🌍 Region", all_regions, default=all_regions)

    # Customer Segment Filter
    all_segments = sorted(raw_df["customer_segment"].dropna().unique().tolist())
    selected_segments = st.multiselect("👥 Customer Segment", all_segments, default=all_segments)

    # Payment Method Filter
    all_payments = sorted(raw_df["payment_method"].dropna().unique().tolist())
    selected_payments = st.multiselect("💳 Payment Method", all_payments, default=all_payments)

    # Return Status Filter
    return_status_option = st.radio(
        "🔄 Return Filter",
        options=["All Orders", "Completed Only", "Returned Only"],
        horizontal=True,
    )

    st.markdown("---")
    st.caption("E-Commerce Order & Return Intelligence v2.0")


# -------------------------------------------------------------
# FILTER LOGIC
# -------------------------------------------------------------
filtered_df = raw_df.copy()

if selected_date_range and len(selected_date_range) == 2:
    start_d, end_d = selected_date_range
    filtered_df = filtered_df[
        (filtered_df["order_date"].dt.date >= start_d)
        & (filtered_df["order_date"].dt.date <= end_d)
    ]

if selected_categories:
    filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]
else:
    filtered_df = filtered_df.iloc[0:0]

if selected_regions:
    filtered_df = filtered_df[filtered_df["region"].isin(selected_regions)]
else:
    filtered_df = filtered_df.iloc[0:0]

if selected_segments:
    filtered_df = filtered_df[filtered_df["customer_segment"].isin(selected_segments)]
else:
    filtered_df = filtered_df.iloc[0:0]

if selected_payments:
    filtered_df = filtered_df[filtered_df["payment_method"].isin(selected_payments)]
else:
    filtered_df = filtered_df.iloc[0:0]

if return_status_option == "Completed Only":
    filtered_df = filtered_df[~filtered_df["is_returned"]]
elif return_status_option == "Returned Only":
    filtered_df = filtered_df[filtered_df["is_returned"]]

if filtered_df.empty:
    st.warning("⚠️ No data matches the selected filter criteria. Please broaden your selection.")
    st.stop()


# -------------------------------------------------------------
# TOP BANNER: CORE BUSINESS KPIS
# -------------------------------------------------------------
kpis = calculate_sales_kpis(filtered_df)

st.title("🛒 E-Commerce Sales, Returns & Customer Analysis")
st.markdown("Comprehensive Business Intelligence, Root Cause Return Patterns & Customer Purchasing Dynamics")

kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)

with kpi_col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Gross Sales (Invoiced)</div>
            <div class="metric-value">Rs. {kpis['gross_sales']:,.0f}</div>
            <div class="metric-subtitle">Total Value Ordered</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Net Sales (Realized)</div>
            <div class="metric-value" style="color: #16a34a;">Rs. {kpis['net_sales']:,.0f}</div>
            <div class="metric-subtitle">Realization: {kpis['net_revenue_realization_rate']:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_col3:
    rate_color = "#ef4444" if kpis["order_return_rate_pct"] > 22 else "#f59e0b" if kpis["order_return_rate_pct"] > 15 else "#10b981"
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Order Return Rate</div>
            <div class="metric-value" style="color: {rate_color};">{kpis['order_return_rate_pct']:.1f}%</div>
            <div class="metric-subtitle">{kpis['returned_orders']:,} returned orders</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Refund Loss</div>
            <div class="metric-value" style="color: #dc2626;">Rs. {kpis['total_refunds']:,.0f}</div>
            <div class="metric-subtitle">{kpis['sales_return_rate_pct']:.1f}% of gross revenue</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_col5:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Total Orders & Units</div>
            <div class="metric-value">{kpis['total_orders']:,}</div>
            <div class="metric-subtitle">{kpis['total_units_sold']:,} total units sold</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_col6:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Avg Order Value (AOV)</div>
            <div class="metric-value">Rs. {kpis['aov_gross']:,.0f}</div>
            <div class="metric-subtitle">Net AOV: Rs. {kpis['aov_net']:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)


# -------------------------------------------------------------
# TAB NAVIGATION
# -------------------------------------------------------------
tab_overview, tab_sales, tab_cust, tab_prod, tab_returns, tab_anomalies, tab_data = st.tabs([
    "📊 Executive Overview",
    "📈 Sales Performance",
    "👥 Customer Purchasing Behaviour",
    "📦 Product & Category Analytics",
    "🔄 Return Behaviour & Root Cause",
    "🚨 Strategic Insights & Anomalies",
    "📋 Data Explorer & Export",
])


# -------------------------------------------------------------
# TAB 1: EXECUTIVE OVERVIEW
# -------------------------------------------------------------
with tab_overview:
    st.subheader("Executive Performance Summary")
    
    col_chart, col_highlights = st.columns([2, 1])

    with col_chart:
        # Monthly Gross vs Net Sales & Return Rate
        monthly_df = (
            filtered_df.groupby("order_year_month")
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
        monthly_df["return_rate"] = (monthly_df["returns"] / monthly_df["orders"] * 100).round(1)

        fig_overview = make_subplots(specs=[[{"secondary_y": True}]])

        fig_overview.add_trace(
            go.Bar(
                x=monthly_df["order_year_month"],
                y=monthly_df["gross_sales"],
                name="Gross Sales (Rs.)",
                marker_color="#93c5fd",
                opacity=0.8,
            ),
            secondary_y=False,
        )

        fig_overview.add_trace(
            go.Bar(
                x=monthly_df["order_year_month"],
                y=monthly_df["net_sales"],
                name="Net Realized Sales (Rs.)",
                marker_color="#10b981",
            ),
            secondary_y=False,
        )

        fig_overview.add_trace(
            go.Scatter(
                x=monthly_df["order_year_month"],
                y=monthly_df["return_rate"],
                name="Return Rate (%)",
                mode="lines+markers",
                line=dict(color="#ef4444", width=3),
                marker=dict(size=8),
            ),
            secondary_y=True,
        )

        fig_overview.update_layout(
            title="Monthly Revenue Realization & Return Rate Trend",
            barmode="group",
            xaxis_title="Month",
            yaxis_title="Revenue (Rs.)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=430,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        fig_overview.update_yaxes(title_text="Revenue (Rs.)", secondary_y=False)
        fig_overview.update_yaxes(title_text="Return Rate (%)", secondary_y=True, range=[0, 45])
        st.plotly_chart(fig_overview, use_container_width=True)

    with col_highlights:
        st.markdown("#### ⚡ Core Findings at a Glance")
        
        realized_pct = kpis["net_revenue_realization_rate"]
        
        st.info(f"**Revenue Realization:** Out of Rs. {kpis['gross_sales']:,.0f} gross sales, **Rs. {kpis['net_sales']:,.0f} ({realized_pct:.1f}%)** was retained after accounting for Rs. {kpis['total_refunds']:,.0f} in return refunds.")
        
        cat_ret = filtered_df.groupby("category").agg(
            orders=("order_id", "nunique"),
            returns=("is_returned", "sum")
        ).reset_index()
        cat_ret["rate"] = cat_ret["returns"] / cat_ret["orders"] * 100
        worst_cat = cat_ret.sort_values("rate", ascending=False).iloc[0]
        
        st.warning(f"**Highest Return Category:** **{worst_cat['category']}** leads returns with an order return rate of **{worst_cat['rate']:.1f}%**.")

        cod_data = filtered_df[filtered_df["payment_method"] == "Cash on Delivery"]
        if not cod_data.empty:
            cod_rate = (cod_data["is_returned"].mean() * 100)
            st.error(f"**Cash on Delivery Risk:** COD orders exhibit a **{cod_rate:.1f}%** return/rejection rate, consistently higher than digital prepaid payment channels.")

    st.markdown("#### Revenue Retention & Refund Erosion by Product Category")
    cat_summary = (
        filtered_df.groupby("category")
        .agg(
            gross_sales=("gross_sales", "sum"),
            net_sales=("net_sales", "sum"),
            refunds=("refund_amount", "sum"),
            return_rate=("is_returned", lambda x: x.mean() * 100),
        )
        .reset_index()
        .sort_values("gross_sales", ascending=False)
    )

    fig_cat_bar = px.bar(
        cat_summary,
        x="category",
        y=["net_sales", "refunds"],
        title="Gross Revenue Breakdown: Net Realized Sales vs Refunded Loss (Rs.)",
        labels={"value": "Amount (Rs.)", "category": "Product Category", "variable": "Revenue Component"},
        color_discrete_map={"net_sales": "#10b981", "refunds": "#f87171"},
        barmode="stack",
        height=380,
    )
    st.plotly_chart(fig_cat_bar, use_container_width=True)


# -------------------------------------------------------------
# TAB 2: SALES PERFORMANCE
# -------------------------------------------------------------
with tab_sales:
    st.subheader("Sales Performance & Revenue Breakdown")

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        region_sales = (
            filtered_df.groupby("region")
            .agg(gross_sales=("gross_sales", "sum"), net_sales=("net_sales", "sum"), orders=("order_id", "nunique"))
            .reset_index()
            .sort_values("net_sales", ascending=False)
        )
        fig_region = px.pie(
            region_sales,
            names="region",
            values="net_sales",
            title="Net Realized Sales Share by Region",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Pastel,
            height=380,
        )
        st.plotly_chart(fig_region, use_container_width=True)

    with col_s2:
        subcat_sales = (
            filtered_df.groupby(["category", "sub_category"])
            .agg(net_sales=("net_sales", "sum"), units=("quantity", "sum"))
            .reset_index()
        )
        fig_treemap = px.treemap(
            subcat_sales,
            path=["category", "sub_category"],
            values="net_sales",
            title="Net Sales Distribution across Categories & Sub-Categories",
            color="net_sales",
            color_continuous_scale="Blues",
            height=380,
        )
        st.plotly_chart(fig_treemap, use_container_width=True)

    st.markdown("#### Sales Velocity Over Time")
    granularity = st.radio("Group Time-Series By:", ["Weekly", "Monthly", "Daily"], horizontal=True)
    
    time_df = filtered_df.copy()
    if granularity == "Daily":
        time_df["time_period"] = time_df["order_date"].dt.date
    elif granularity == "Weekly":
        time_df["time_period"] = time_df["order_date"].dt.to_period("W").dt.start_time
    else:
        time_df["time_period"] = time_df["order_date"].dt.to_period("M").dt.start_time

    time_grouped = (
        time_df.groupby("time_period")
        .agg(gross_sales=("gross_sales", "sum"), net_sales=("net_sales", "sum"), orders=("order_id", "nunique"))
        .reset_index()
        .sort_values("time_period")
    )

    fig_time = px.area(
        time_grouped,
        x="time_period",
        y=["gross_sales", "net_sales"],
        title=f"{granularity} Sales Invoiced vs Realized (Rs.)",
        labels={"value": "Amount (Rs.)", "time_period": "Date", "variable": "Sales Type"},
        color_discrete_map={"gross_sales": "#93c5fd", "net_sales": "#3b82f6"},
        height=380,
    )
    st.plotly_chart(fig_time, use_container_width=True)


# -------------------------------------------------------------
# TAB 3: CUSTOMER PURCHASING BEHAVIOUR & RFM
# -------------------------------------------------------------
with tab_cust:
    st.subheader("Customer Purchasing Patterns & RFM Segmentation")
    
    cust_analysis = analyze_customer_purchasing_behaviour(filtered_df)
    cust_df = cust_analysis["customer_summary"]

    col_c1, col_c2, col_c3 = st.columns(3)
    col_c1.metric("Unique Customers", f"{cust_analysis['total_unique_customers']:,}")
    col_c2.metric("Repeat Purchase Rate", f"{cust_analysis['repeat_rate_pct']}%")
    col_c3.metric("Serial Returners Identified", f"{cust_analysis['serial_returners_count']} accounts")

    col_rfm_chart, col_freq_chart = st.columns([3, 2])

    with col_rfm_chart:
        rfm_summary = cust_analysis["rfm_segment_stats"]
        fig_rfm = px.bar(
            rfm_summary,
            x="rfm_segment",
            y="customer_count",
            color="avg_return_rate",
            color_continuous_scale="Reds",
            title="Customer RFM Segments (Color = Avg Return Rate %)",
            labels={"rfm_segment": "Segment", "customer_count": "Number of Customers", "avg_return_rate": "Avg Return %"},
            text_auto=True,
            height=380,
        )
        st.plotly_chart(fig_rfm, use_container_width=True)

    with col_freq_chart:
        order_counts = cust_df["total_orders"].value_counts().reset_index()
        order_counts.columns = ["orders_placed", "customer_count"]
        order_counts = order_counts.sort_values("orders_placed")

        fig_freq = px.bar(
            order_counts,
            x="orders_placed",
            y="customer_count",
            title="Customer Order Frequency Distribution",
            labels={"orders_placed": "Orders Placed", "customer_count": "Customers"},
            color_discrete_sequence=["#6366f1"],
            text_auto=True,
            height=380,
        )
        st.plotly_chart(fig_freq, use_container_width=True)

    st.markdown("#### Customer Gross Spend vs. Return Propensity")
    fig_cust_scatter = px.scatter(
        cust_df,
        x="total_gross_spend",
        y="return_rate_pct",
        size="total_orders",
        color="customer_segment",
        hover_name="customer_name",
        hover_data=["customer_id", "total_orders", "total_net_spend"],
        title="Customer Value vs Return Rate Matrix (Bubble size = Order count)",
        labels={"total_gross_spend": "Gross Spend (Rs.)", "return_rate_pct": "Return Rate (%)", "customer_segment": "Segment"},
        height=420,
    )
    fig_cust_scatter.add_hline(y=50, line_dash="dash", line_color="red", annotation_text="High Risk Return Threshold (50%)")
    st.plotly_chart(fig_cust_scatter, use_container_width=True)


# -------------------------------------------------------------
# TAB 4: PRODUCT & CATEGORY ANALYTICS
# -------------------------------------------------------------
with tab_prod:
    st.subheader("Product Performance Matrix & Category Dynamics")

    prod_analysis = analyze_product_performance(filtered_df)
    all_prods = prod_analysis["all_products"]

    st.markdown("#### Product Portfolio Matrix: Volume vs. Return Rate")
    fig_prod_matrix = px.scatter(
        all_prods,
        x="gross_sales",
        y="return_rate_pct",
        size="units_sold",
        color="category",
        hover_name="product_name",
        hover_data=["sub_category", "net_sales", "refunds", "total_orders"],
        title="Sales vs Return Rate Bubble Chart (Size = Units Sold)",
        labels={"gross_sales": "Gross Sales (Rs.)", "return_rate_pct": "Return Rate (%)"},
        height=450,
    )
    fig_prod_matrix.add_hline(y=20, line_dash="dot", line_color="orange", annotation_text="20% Caution Line")
    fig_prod_matrix.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="30% High Return Critical Threshold")
    st.plotly_chart(fig_prod_matrix, use_container_width=True)

    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown("##### 🏆 Top 10 Products by Realized Net Sales")
        top10_net = prod_analysis["top_by_net_sales"].head(10)[["product_name", "category", "net_sales", "return_rate_pct"]]
        top10_net.columns = ["Product", "Category", "Net Sales (Rs.)", "Return Rate %"]
        top10_net["Net Sales (Rs.)"] = top10_net["Net Sales (Rs.)"].apply(lambda x: f"Rs. {x:,.0f}")
        top10_net["Return Rate %"] = top10_net["Return Rate %"].apply(lambda x: f"{x:.1f}%")
        st.dataframe(top10_net, use_container_width=True, hide_index=True)

    with col_p2:
        st.markdown("##### ⚠️ Products with Highest Return Rates (Min 10 Orders)")
        high_ret_p = all_prods[all_prods["total_orders"] >= 10].sort_values("return_rate_pct", ascending=False).head(10)
        high_ret_p = high_ret_p[["product_name", "category", "total_orders", "return_rate_pct", "refunds"]]
        high_ret_p.columns = ["Product", "Category", "Orders", "Return Rate %", "Refund Loss (Rs.)"]
        high_ret_p["Refund Loss (Rs.)"] = high_ret_p["Refund Loss (Rs.)"].apply(lambda x: f"Rs. {x:,.0f}")
        high_ret_p["Return Rate %"] = high_ret_p["Return Rate %"].apply(lambda x: f"{x:.1f}%")
        st.dataframe(high_ret_p, use_container_width=True, hide_index=True)


# -------------------------------------------------------------
# TAB 5: RETURN BEHAVIOUR & ROOT CAUSE
# -------------------------------------------------------------
with tab_returns:
    st.subheader("Return Behaviour & Root Cause Deep Dive")

    ret_analysis = analyze_return_behaviour(filtered_df)

    col_r1, col_r2 = st.columns(2)

    with col_r1:
        reasons_df = ret_analysis["reasons_overall"]
        fig_reasons = px.pie(
            reasons_df,
            names="return_reason",
            values="return_count",
            title="Primary Return Drivers (Share of All Returns)",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Safe,
            height=380,
        )
        st.plotly_chart(fig_reasons, use_container_width=True)

    with col_r2:
        pm_df = ret_analysis["payment_returns"]
        fig_pm = px.bar(
            pm_df,
            x="payment_method",
            y="return_rate_pct",
            title="Return / Rejection Rate by Payment Method (%)",
            labels={"payment_method": "Payment Method", "return_rate_pct": "Return Rate (%)"},
            color="return_rate_pct",
            color_continuous_scale="Reds",
            text_auto=True,
            height=380,
        )
        st.plotly_chart(fig_pm, use_container_width=True)

    col_r3, col_r4 = st.columns(2)

    with col_r3:
        reasons_cat = ret_analysis["reasons_by_category"]
        fig_rcat = px.bar(
            reasons_cat,
            x="category",
            y="count",
            color="return_reason",
            title="Return Reasons Breakdown by Product Category",
            labels={"category": "Category", "count": "Returned Orders", "return_reason": "Reason"},
            barmode="stack",
            height=380,
        )
        st.plotly_chart(fig_rcat, use_container_width=True)

    with col_r4:
        ret_orders = filtered_df[filtered_df["is_returned"] & filtered_df["days_to_return"].notna()]
        fig_days = px.histogram(
            ret_orders,
            x="days_to_return",
            nbins=14,
            title="Distribution of Days to Return (Order to Return Initiation)",
            labels={"days_to_return": "Days to Return"},
            color_discrete_sequence=["#f97316"],
            height=380,
        )
        st.plotly_chart(fig_days, use_container_width=True)


# -------------------------------------------------------------
# TAB 6: STRATEGIC INSIGHTS & ANOMALIES
# -------------------------------------------------------------
with tab_anomalies:
    st.subheader("Automated Anomaly Detection & Business Recommendations")

    insights_list = detect_anomalies_and_insights(filtered_df)

    for item in insights_list:
        css_class = "badge-alert" if item["level"] == "Critical" else "badge-warning" if item["level"] in ["Alert", "Warning"] else "badge-info"
        badge_symbol = "🚨" if item["level"] == "Critical" else "⚠️" if item["level"] in ["Alert", "Warning"] else "💡"
        
        st.markdown(
            f"""
            <div class="{css_class}">
                <h4 style="margin: 0 0 6px 0;">{badge_symbol} [{item['level'].upper()}] {item['type']}</h4>
                <p style="margin: 0 0 8px 0; font-size: 0.95rem;"><strong>Observation:</strong> {item['finding']}</p>
                <p style="margin: 0; font-size: 0.92rem; color: #1e293b;"><strong>Recommended Strategic Action:</strong> {item['recommendation']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("#### Strategic Action Roadmap for E-Commerce Stakeholders")
    
    st_col1, st_col2, st_col3 = st.columns(3)
    with st_col1:
        st.markdown(
            """
            **1. Merchandising & Sizing**
            - Standardize sizing charts with detailed 3D fit guides for Apparel & Footwear.
            - Introduce user sizing reviews ("Runs true to size / Runs small").
            """
        )
    with st_col2:
        st.markdown(
            """
            **2. Checkout & Payment Optimization**
            - Offer 2-3% instant UPI discount to switch customers away from COD.
            - Send SMS/WhatsApp confirmation before dispatching COD packages.
            """
        )
    with st_col3:
        st.markdown(
            """
            **3. Reverse Logistics & QA**
            - Implement pre-dispatch visual checks for high-return electronic models.
            - Institute return fee or threshold for identified serial returner accounts.
            """
        )


# -------------------------------------------------------------
# TAB 7: DATA EXPLORER & EXPORT
# -------------------------------------------------------------
with tab_data:
    st.subheader("Data Explorer & Export")
    st.caption("Search, filter, inspect, and download cleaned order and return records.")

    search_query = st.text_input("🔍 Search orders by Customer Name, Order ID, or Product Name:", "")

    display_df = filtered_df.copy()
    if search_query:
        mask = (
            display_df["order_id"].astype(str).str.contains(search_query, case=False, na=False)
            | display_df["customer_name"].astype(str).str.contains(search_query, case=False, na=False)
            | display_df["product_name"].astype(str).str.contains(search_query, case=False, na=False)
        )
        display_df = display_df[mask]

    cols_to_show = [
        "order_id", "order_date", "customer_name", "region", "product_name",
        "category", "quantity", "gross_sales", "payment_method", "return_status",
        "return_reason", "days_to_return", "net_sales"
    ]
    existing_cols = [c for c in cols_to_show if c in display_df.columns]

    st.dataframe(display_df[existing_cols].head(500), use_container_width=True)
    st.caption(f"Displaying top {min(len(display_df), 500)} of {len(display_df):,} matching rows.")

    csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_bytes,
        file_name="ecommerce_sales_and_returns_filtered.csv",
        mime="text/csv",
    )
