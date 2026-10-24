"""
Aesthetic Presentation Deck Generator:
Creates a visually stunning, modern, easy-to-present 10-slide deck
for the E-Commerce Sales, Returns, and Customer Analysis Project.

Includes:
- High-res embedded statistical charts (Donut, Combo trend, Category benchmarks, Risk bars)
- Modern Midnight Cyber / Glassmorphic Executive Template
- Visual icons and status pills (💰, 💳, 🔄, 📦, 👥, 🏆, 👕, 🚨, 💡, 🎯)
- Built-in 'What to Say' presentation scripts on every slide
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "ecommerce_orders_and_returns.csv"
ASSETS_DIR = BASE_DIR / "assets" / "slides_charts"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

PRIMARY_FILE = BASE_DIR / "Aesthetic_Ecommerce_Presentation.pptx"
SECONDARY_FILE = BASE_DIR / "Simple_Easy_Present_Ecommerce_Analysis.pptx"


# -------------------------------------------------------------
# 1. GENERATE HIGH-RES AESTHETIC CHARTS WITH MATPLOTLIB
# -------------------------------------------------------------
def generate_slide_charts(df):
    """Generate high-resolution dark-themed aesthetic charts for slides."""
    # Chart styling constants
    plt.style.use("dark_background")
    BG_HEX = "#1E293B"      # Matching Card Background
    TEXT_HEX = "#F8FAFC"    # Crisp White
    MUTED_HEX = "#94A3B8"   # Slate Gray
    
    # ---------------------------------------------------------
    # Chart 1: Slide 4 - Revenue Realization Donut
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(4.8, 4.0), facecolor=BG_HEX)
    ax.set_facecolor(BG_HEX)
    
    values = [38527628, 11115644]
    labels = ["Net Realized\n(77.6%)", "Refund Loss\n(22.4%)"]
    colors = ["#10B981", "#EF4444"]
    explode = (0.02, 0.06)

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        explode=explode,
        pctdistance=0.75,
        textprops={"color": TEXT_HEX, "fontsize": 10, "fontweight": "bold"},
        wedgeprops={"width": 0.42, "edgecolor": "#0F172A", "linewidth": 2}
    )
    for at in autotexts:
        at.set_color("#FFFFFF")
        at.set_fontsize(11)

    ax.text(0, 0, "Gross Sales\nRs. 4.96 Cr", ha="center", va="center", color=TEXT_HEX, fontsize=11, fontweight="bold")
    ax.set_title("Revenue Realization vs Refund Loss", color=TEXT_HEX, fontsize=12, fontweight="bold", pad=10)
    plt.tight_layout()
    chart1_path = ASSETS_DIR / "chart_revenue_donut.png"
    plt.savefig(chart1_path, dpi=220, facecolor=BG_HEX)
    plt.close()

    # ---------------------------------------------------------
    # Chart 2: Slide 5 - Monthly Sales Velocity & Return Trend
    # ---------------------------------------------------------
    fig, ax1 = plt.subplots(figsize=(5.4, 3.8), facecolor=BG_HEX)
    ax1.set_facecolor(BG_HEX)
    
    df["month_str"] = pd.to_datetime(df["Order_Date"]).dt.strftime("%b %y")
    monthly = df.groupby("month_str", sort=False).agg(
        gross=("Gross_Sales", "sum"),
        net=("Net_Sales", "sum"),
        ret_rate=("Return_Status", lambda s: (s == "Returned").mean() * 100)
    ).tail(8)

    x = np.arange(len(monthly))
    width = 0.36

    ax1.bar(x - width/2, monthly["gross"] / 100000, width, label="Gross Sales (Rs. L)", color="#60A5FA", alpha=0.9)
    ax1.bar(x + width/2, monthly["net"] / 100000, width, label="Net Realized (Rs. L)", color="#10B981", alpha=0.9)
    ax1.set_ylabel("Sales (Rs. Lakhs)", color=TEXT_HEX, fontsize=9, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(monthly.index, rotation=35, color=MUTED_HEX, fontsize=8, ha="right")
    ax1.tick_params(colors=MUTED_HEX)
    ax1.grid(color="#334155", linestyle="--", linewidth=0.5, alpha=0.7)

    # Secondary Axis for Return Rate line
    ax2 = ax1.twinx()
    ax2.plot(x, monthly["ret_rate"], color="#F43F5E", marker="o", linewidth=2.2, markersize=5, label="Return Rate %")
    ax2.set_ylabel("Return %", color="#F43F5E", fontsize=9, fontweight="bold")
    ax2.set_ylim(10, 35)
    ax2.tick_params(colors="#F43F5E")

    ax1.set_title("Monthly Revenue & Return Velocity", color=TEXT_HEX, fontsize=11, fontweight="bold", pad=8)
    plt.tight_layout()
    chart2_path = ASSETS_DIR / "chart_monthly_trend.png"
    plt.savefig(chart2_path, dpi=220, facecolor=BG_HEX)
    plt.close()

    # ---------------------------------------------------------
    # Chart 3: Slide 6 - Customer RFM Segments
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(5.0, 3.8), facecolor=BG_HEX)
    ax.set_facecolor(BG_HEX)
    
    segments = ["Champions & VIPs", "Loyal Buyers", "Potential Loyal", "At-Risk", "Serial Returners"]
    cust_shares = [38, 28, 18, 10, 6]  # Revenue or share impact
    colors_rfm = ["#6366F1", "#10B981", "#06B6D4", "#F59E0B", "#EF4444"]

    y_pos = np.arange(len(segments))
    bars = ax.barh(y_pos, cust_shares, color=colors_rfm, height=0.55, edgecolor="#0F172A", linewidth=1.2)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(segments, color=TEXT_HEX, fontsize=9, fontweight="bold")
    ax.set_xlabel("Net Revenue Contribution (%)", color=MUTED_HEX, fontsize=9, fontweight="bold")
    ax.set_title("Customer Segments & Revenue Impact", color=TEXT_HEX, fontsize=11, fontweight="bold", pad=8)
    ax.grid(color="#334155", linestyle="--", linewidth=0.5, axis="x", alpha=0.7)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 1.2, bar.get_y() + bar.get_height()/2, f"{w}%", va="center", color=TEXT_HEX, fontsize=9, fontweight="bold")

    ax.set_xlim(0, 48)
    plt.tight_layout()
    chart3_path = ASSETS_DIR / "chart_customer_rfm.png"
    plt.savefig(chart3_path, dpi=220, facecolor=BG_HEX)
    plt.close()

    # ---------------------------------------------------------
    # Chart 4: Slide 7 - Category Return Rate Benchmark
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(5.2, 3.8), facecolor=BG_HEX)
    ax.set_facecolor(BG_HEX)

    cats = ["Clothing & Apparel", "Home & Furniture", "Sports & Fitness", "Electronics", "Beauty & Care"]
    ret_rates = [34.5, 21.0, 19.8, 18.9, 11.9]
    colors_cat = ["#EF4444", "#F59E0B", "#F59E0B", "#06B6D4", "#10B981"]

    y_pos = np.arange(len(cats))
    bars = ax.barh(y_pos, ret_rates, color=colors_cat, height=0.52, edgecolor="#0F172A", linewidth=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(cats, color=TEXT_HEX, fontsize=9, fontweight="bold")
    ax.set_xlabel("Return Rate (%)", color=MUTED_HEX, fontsize=9, fontweight="bold")
    ax.set_title("Return Rate Benchmark by Category", color=TEXT_HEX, fontsize=11, fontweight="bold", pad=8)
    ax.axvline(20, color="#94A3B8", linestyle=":", linewidth=1.2, alpha=0.8, label="20% Threshold")
    ax.grid(color="#334155", linestyle="--", linewidth=0.5, axis="x", alpha=0.7)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.8, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", va="center", color=TEXT_HEX, fontsize=9, fontweight="bold")

    ax.set_xlim(0, 42)
    plt.tight_layout()
    chart4_path = ASSETS_DIR / "chart_category_returns.png"
    plt.savefig(chart4_path, dpi=220, facecolor=BG_HEX)
    plt.close()

    # ---------------------------------------------------------
    # Chart 5: Slide 8 - Return Root Causes Donut
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(4.8, 4.0), facecolor=BG_HEX)
    ax.set_facecolor(BG_HEX)

    causes = ["Size / Fit", "Defective", "Not Described", "Changed Mind", "Late Delivery"]
    cause_vals = [28.3, 22.0, 18.1, 15.4, 16.2]
    cause_colors = ["#EF4444", "#F59E0B", "#8B5CF6", "#3B82F6", "#64748B"]

    wedges, texts, autotexts = ax.pie(
        cause_vals,
        labels=causes,
        autopct="%1.1f%%",
        startangle=130,
        colors=cause_colors,
        pctdistance=0.75,
        textprops={"color": TEXT_HEX, "fontsize": 8.5, "fontweight": "bold"},
        wedgeprops={"width": 0.44, "edgecolor": "#0F172A", "linewidth": 1.5}
    )
    for at in autotexts:
        at.set_color("#FFFFFF")
        at.set_fontsize(8.5)

    ax.text(0, 0, "Top Reason:\nSize & Fit\n(28.3%)", ha="center", va="center", color="#EF4444", fontsize=9.5, fontweight="bold")
    ax.set_title("Stated Return Drivers (1,135 Returns)", color=TEXT_HEX, fontsize=11, fontweight="bold", pad=8)
    plt.tight_layout()
    chart5_path = ASSETS_DIR / "chart_return_reasons.png"
    plt.savefig(chart5_path, dpi=220, facecolor=BG_HEX)
    plt.close()

    # ---------------------------------------------------------
    # Chart 6: Slide 9 - Payment Method COD Risk
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(5.0, 3.8), facecolor=BG_HEX)
    ax.set_facecolor(BG_HEX)

    pay_methods = ["Cash on Delivery", "Debit Card", "Credit Card", "UPI / Wallets", "Net Banking"]
    pay_rates = [31.8, 21.1, 20.4, 19.6, 18.5]
    colors_pm = ["#EF4444", "#94A3B8", "#60A5FA", "#10B981", "#94A3B8"]

    x_pos = np.arange(len(pay_methods))
    bars = ax.bar(x_pos, pay_rates, color=colors_pm, width=0.55, edgecolor="#0F172A", linewidth=1)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(["COD\n(Critical)", "Debit\nCard", "Credit\nCard", "UPI\n(Lowest)", "Net\nBanking"], color=TEXT_HEX, fontsize=8.5, fontweight="bold")
    ax.set_ylabel("Return Rate (%)", color=MUTED_HEX, fontsize=9, fontweight="bold")
    ax.set_title("Return Rate by Payment Method (%)", color=TEXT_HEX, fontsize=11, fontweight="bold", pad=8)
    ax.axhline(20.0, color="#10B981", linestyle="--", linewidth=1.2, alpha=0.8, label="Digital Baseline (~20%)")
    ax.grid(color="#334155", linestyle="--", linewidth=0.5, axis="y", alpha=0.7)

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.8, f"{h:.1f}%", ha="center", color=TEXT_HEX, fontsize=8.5, fontweight="bold")

    ax.set_ylim(0, 38)
    plt.tight_layout()
    chart6_path = ASSETS_DIR / "chart_payment_risk.png"
    plt.savefig(chart6_path, dpi=220, facecolor=BG_HEX)
    plt.close()

    # ---------------------------------------------------------
    # Chart 7: Slide 10 - Return Reduction & Profit Recovery
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(5.0, 3.8), facecolor=BG_HEX)
    ax.set_facecolor(BG_HEX)

    scenarios = ["Current State\n(22.7% Returns)", "Target State\n(17.7% Returns)", "Margin\nRecovered"]
    vals_loss = [111.1, 86.6, 24.5]
    colors_sc = ["#EF4444", "#3B82F6", "#10B981"]

    x_pos = np.arange(len(scenarios))
    bars = ax.bar(x_pos, vals_loss, color=colors_sc, width=0.5, edgecolor="#0F172A", linewidth=1)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(scenarios, color=TEXT_HEX, fontsize=8.5, fontweight="bold")
    ax.set_ylabel("Refund Amount (Rs. Lakhs)", color=MUTED_HEX, fontsize=9, fontweight="bold")
    ax.set_title("Annual Profit Recovery Potential", color=TEXT_HEX, fontsize=11, fontweight="bold", pad=8)
    ax.grid(color="#334155", linestyle="--", linewidth=0.5, axis="y", alpha=0.7)

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 2.0, f"Rs. {h:.1f}L", ha="center", color=TEXT_HEX, fontsize=9, fontweight="bold")

    ax.set_ylim(0, 130)
    plt.tight_layout()
    chart7_path = ASSETS_DIR / "chart_roi_recovery.png"
    plt.savefig(chart7_path, dpi=220, facecolor=BG_HEX)
    plt.close()

    return {
        "donut": chart1_path,
        "monthly": chart2_path,
        "rfm": chart3_path,
        "category": chart4_path,
        "reasons": chart5_path,
        "payment": chart6_path,
        "roi": chart7_path,
    }


# -------------------------------------------------------------
# 2. BUILD THE AESTHETIC 10-SLIDE DECK
# -------------------------------------------------------------
def build_aesthetic_deck():
    df = pd.read_csv(DATA_FILE)
    charts = generate_slide_charts(df)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Aesthetic Theme Palette (Midnight Navy & Electric Accents)
    COLOR_BG = RGBColor(11, 15, 25)            # Deep Space Navy #0B0F19
    COLOR_CARD = RGBColor(30, 41, 59)          # Card Slate #1E293B
    COLOR_BORDER = RGBColor(51, 65, 85)        # Card Border #334155
    COLOR_TEXT_MAIN = RGBColor(248, 250, 252)  # Pure White #F8FAFC
    COLOR_TEXT_MUTED = RGBColor(148, 163, 184) # Slate Muted #94A3B8

    COLOR_INDIGO = RGBColor(99, 102, 241)      # Indigo #6366F1
    COLOR_EMERALD = RGBColor(16, 185, 129)     # Emerald #10B981
    COLOR_ROSE = RGBColor(239, 68, 68)         # Rose Red #EF4444
    COLOR_AMBER = RGBColor(245, 158, 11)       # Amber #F59E0B
    COLOR_CYAN = RGBColor(6, 182, 212)         # Cyan #06B6D4

    def apply_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()
        return bg

    def add_card(slide, left, top, width, height, border_col=COLOR_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD
        card.line.color.rgb = border_col
        card.line.width = Pt(1.5)
        return card

    def add_header(slide, slide_num, title, category_tag="E-COMMERCE DATA ANALYSIS"):
        # Tag & Number
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.3))
        tf_tag = tag_box.text_frame
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = f"SLIDE {slide_num} OF 10  •  {category_tag.upper()}"
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_INDIGO

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.65))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(25)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MAIN

        # Subtle divider
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.38), Inches(11.733), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_BORDER
        line.line.fill.background()

    def add_speaker_cue(slide, cue_text):
        cue_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.32), Inches(11.733), Inches(0.8))
        cue_card.fill.solid()
        cue_card.fill.fore_color.rgb = RGBColor(15, 23, 42)
        cue_card.line.color.rgb = COLOR_INDIGO
        cue_card.line.width = Pt(1.2)

        tb = slide.shapes.add_textbox(Inches(1.0), Inches(6.34), Inches(11.3), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = "🗣️ Presenter Script: "
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_INDIGO

        run = p.add_run()
        run.text = f'"{cue_text}"'
        run.font.size = Pt(11)
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================
    # SLIDE 1: AESTHETIC HERO TITLE SLIDE
    # =========================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_bg(s1)

    hero_card = add_card(s1, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5), COLOR_INDIGO)
    
    tb = s1.shapes.add_textbox(Inches(1.8), Inches(1.5), Inches(9.7), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p_badge = tf.paragraphs[0]
    p_badge.text = "📊  ACADEMIC & EXECUTIVE PROJECT PRESENTATION"
    p_badge.font.size = Pt(12)
    p_badge.font.bold = True
    p_badge.font.color.rgb = COLOR_INDIGO
    p_badge.space_after = Pt(14)

    p_title = tf.add_paragraph()
    p_title.text = "E-Commerce Sales, Returns &\nCustomer Behaviour Analysis"
    p_title.font.size = Pt(38)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_TEXT_MAIN
    p_title.space_after = Pt(16)

    p_sub = tf.add_paragraph()
    p_sub.text = "Understanding Revenue Realization, Customer RFM Loyalty & Return Root-Causes"
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = COLOR_TEXT_MUTED
    p_sub.space_after = Pt(28)

    p_meta = tf.add_paragraph()
    p_meta.text = "📁 Dataset: Kaggle E-Commerce Orders & Returns  •  🛠️ Stack: Python, Pandas, Streamlit, Matplotlib"
    p_meta.font.size = Pt(13)
    p_meta.font.bold = True
    p_meta.font.color.rgb = COLOR_EMERALD

    # =========================================================
    # SLIDE 2: PROJECT OVERVIEW & PROBLEM STATEMENT
    # =========================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_bg(s2)
    add_header(s2, "2", "Project Overview & Business Problem", "THE CONTEXT")

    cards_s2 = [
        ("🚨 The Real-World Problem", "High gross sales look impressive on paper, but product returns quietly destroy company profit margins. Returns cause extra delivery costs, restocking fees, and tied-up stock.", COLOR_ROSE),
        ("💸 Why It Matters", "Our analysis reveals a 22.7% return rate — meaning over 1 Crore Rupees was lost to customer refunds. We need to identify exactly which items get returned and why.", COLOR_AMBER),
        ("🎯 Project Objectives", "• Clean & validate 5,000 order records\n• Analyze sales velocity and revenue trends\n• Profile customer purchasing behaviour (RFM)\n• Uncover return causes and deliver solutions", COLOR_EMERALD)
    ]

    for i, (title, desc, col) in enumerate(cards_s2):
        left = Inches(0.8 + i * 3.98)
        add_card(s2, left, Inches(1.6), Inches(3.8), Inches(4.5), col)
        tb = s2.shapes.add_textbox(left + Inches(0.2), Inches(1.8), Inches(3.4), Inches(4.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(12)

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(13)
        p_desc.font.color.rgb = COLOR_TEXT_MAIN

    add_speaker_cue(
        s2,
        "Good morning everyone. In this project, we analyzed an e-commerce platform to understand where the company generates strong sales, and where it loses significant revenue due to product returns."
    )

    # =========================================================
    # SLIDE 3: DATASET ARCHITECTURE & QUALITY
    # =========================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_bg(s3)
    add_header(s3, "3", "Dataset Architecture & Data Pipeline", "DATA PREPARATION")

    badges = [
        ("📦 5,000", "Total Orders", "15 months analyzed", COLOR_INDIGO),
        ("👥 811", "Unique Customers", "Across 20 Indian cities", COLOR_CYAN),
        ("📋 31", "Features", "Orders, customers, returns", COLOR_AMBER),
        ("✨ 100%", "Clean Data", "Zero duplicates / NaNs", COLOR_EMERALD),
    ]

    for i, (val, title, sub, col) in enumerate(badges):
        left = Inches(0.8 + i * 2.98)
        add_card(s3, left, Inches(1.6), Inches(2.8), Inches(1.5), col)
        tb = s3.shapes.add_textbox(left + Inches(0.15), Inches(1.7), Inches(2.5), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = val
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = col

        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_TEXT_MAIN

        p_s = tf.add_paragraph()
        p_s.text = sub
        p_s.font.size = Pt(10)
        p_s.font.color.rgb = COLOR_TEXT_MUTED

    # Large Bottom Architecture Card
    add_card(s3, Inches(0.8), Inches(3.3), Inches(11.733), Inches(2.8))
    tb_arch = s3.shapes.add_textbox(Inches(1.1), Inches(3.5), Inches(11.1), Inches(2.4))
    tf_arch = tb_arch.text_frame
    tf_arch.word_wrap = True

    p = tf_arch.paragraphs[0]
    p.text = "🛠️ How We Cleaned and Transformed the Dataset:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(8)

    steps_s3 = [
        "1. Timestamp Parsing: Validated Order Date, Delivery Date, and Return Date; calculated delivery and return transit days.",
        "2. Numeric Boundary Checks: Enforced positive Unit Price, Quantity >= 1, and verified gross vs net pricing arithmetic.",
        "3. Missing Value Treatment: Applied zero-loss imputation; marked non-returned orders cleanly as 'Completed' and standardized reasons.",
        "4. Derived Financial Measures: Engineered Net Realized Sales, Refund Loss, Revenue Realization Rate %, and RFM customer scores."
    ]
    for stp in steps_s3:
        p_stp = tf_arch.add_paragraph()
        p_stp.text = stp
        p_stp.font.size = Pt(12)
        p_stp.font.color.rgb = COLOR_TEXT_MAIN
        p_stp.space_after = Pt(3)

    add_speaker_cue(
        s3,
        "We worked with 5,000 orders placed by 811 customers across 31 features. Before running any analysis, we cleaned all missing values, removed duplicate rows, and verified all date calculations."
    )

    # =========================================================
    # SLIDE 4: THE BIG NUMBERS (With Real Donut Chart!)
    # =========================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_bg(s4)
    add_header(s4, "4", "Executive KPIs: The Big Numbers", "REVENUE & REALIZATION")

    # Left Column: Metric Cards
    kpis_col = [
        ("💰 Gross Sales", "Rs. 4.96 Crore", "Total value of all customer orders", COLOR_INDIGO),
        ("💳 Net Realized Sales", "Rs. 3.85 Crore", "Actual cash retained (77.6% realization)", COLOR_EMERALD),
        ("🔄 Order Return Rate", "22.70%", "1,135 orders sent back by customers", COLOR_ROSE),
        ("💸 Total Refund Loss", "Rs. 1.11 Crore", "22.4% direct gross revenue erosion", COLOR_AMBER)
    ]

    for i, (lbl, val, sub, col) in enumerate(kpis_col):
        top = Inches(1.6 + i * 1.12)
        add_card(s4, Inches(0.8), top, Inches(6.5), Inches(1.0), col)
        tb = s4.shapes.add_textbox(Inches(1.0), top + Inches(0.08), Inches(6.1), Inches(0.84))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"{lbl}:  {val}"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = col

        p_s = tf.add_paragraph()
        p_s.text = sub
        p_s.font.size = Pt(11)
        p_s.font.color.rgb = COLOR_TEXT_MUTED

    # Right Column: Donut Chart Image
    add_card(s4, Inches(7.5), Inches(1.6), Inches(5.033), Inches(4.5))
    s4.shapes.add_picture(str(charts["donut"]), Inches(7.6), Inches(1.75), Inches(4.8), Inches(4.1))

    add_speaker_cue(
        s4,
        "Here are the headline numbers: Out of nearly 5 crore rupees in gross sales, over 1.1 crore rupees was refunded because 22.7% of orders were returned. That is nearly 1 in every 4 orders."
    )

    # =========================================================
    # SLIDE 5: SALES PERFORMANCE & TRENDS (With Trend Chart!)
    # =========================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_bg(s5)
    add_header(s5, "5", "Sales Velocity & Monthly Trends", "SEASONALITY & TIMELINE")

    # Left Column: Insights Card
    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.9), Inches(4.5))
    tb_s5 = s5.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.5), Inches(4.1))
    tf_s5 = tb_s5.text_frame
    tf_s5.word_wrap = True

    p = tf_s5.paragraphs[0]
    p.text = "📈 Key Sales & Seasonality Findings:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(10)

    points_s5 = [
        ("Steady Baseline:", "The business maintains a reliable monthly run-rate of approximately Rs. 33 Lakhs."),
        ("Q4 Festival Surge:", "October to December recorded sales exceeding Rs. 38 Lakhs per month fueled by festival promotions."),
        ("The January Hangover:", "Returns spiked sharply in January (reaching 24.5%) as holiday gifts and impulse buys were returned."),
        ("Balanced Geography:", "Demand is well spread: West (27%), North (26%), South (25%), and East (22%).")
    ]
    for title, desc in points_s5:
        p_pt = tf_s5.add_paragraph()
        p_pt.text = f"• {title} "
        p_pt.font.size = Pt(12)
        p_pt.font.bold = True
        p_pt.font.color.rgb = COLOR_TEXT_MAIN
        run = p_pt.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED
        p_pt.space_after = Pt(6)

    # Right Column: Monthly Chart Image
    add_card(s5, Inches(6.9), Inches(1.6), Inches(5.633), Inches(4.5))
    s5.shapes.add_picture(str(charts["monthly"]), Inches(7.0), Inches(1.75), Inches(5.4), Inches(4.1))

    add_speaker_cue(
        s5,
        "Sales were strong year-round with a big peak during the Q4 festival season. However, that holiday shopping rush was immediately followed by a sharp return spike in January."
    )

    # =========================================================
    # SLIDE 6: CUSTOMER LOYALTY & SERIAL RETURNERS (With RFM Chart!)
    # =========================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_bg(s6)
    add_header(s6, "6", "Customer Loyalty vs. Return Abuse", "RFM SEGMENTATION")

    # Left Column: Insights
    add_card(s6, Inches(0.8), Inches(1.6), Inches(6.1), Inches(4.5))
    tb_s6 = s6.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.7), Inches(4.1))
    tf_s6 = tb_s6.text_frame
    tf_s6.word_wrap = True

    p = tf_s6.paragraphs[0]
    p.text = "👥 Customer Behaviour Insights:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_after = Pt(10)

    points_s6 = [
        ("High Loyalty (84% Repeat Rate):", "Most buyers purchase repeatedly, averaging 6.2 orders per account over the 15 months."),
        ("Champions & VIPs (25% of buyers):", "Generate 38% of platform net revenue with an exemplary low return rate of only 14%."),
        ("🚨 The Serial Returners Discovery:", "We detected 53 customers who ordered at least 3 times and returned MORE than 50% of what they bought."),
        ("Rs. 17.4 Lakhs Loss:", "These 53 serial returners caused nearly 16% of all return losses on the entire platform!")
    ]
    for title, desc in points_s6:
        p_pt = tf_s6.add_paragraph()
        p_pt.text = f"• {title} "
        p_pt.font.size = Pt(12)
        p_pt.font.bold = True
        p_pt.font.color.rgb = COLOR_TEXT_MAIN
        run = p_pt.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED
        p_pt.space_after = Pt(6)

    # Right Column: RFM Chart Image
    add_card(s6, Inches(7.1), Inches(1.6), Inches(5.433), Inches(4.5))
    s6.shapes.add_picture(str(charts["rfm"]), Inches(7.2), Inches(1.8), Inches(5.2), Inches(4.0))

    add_speaker_cue(
        s6,
        "Most customers are loyal with an 84% repeat rate. But our segmentation uncovered 53 'serial returners' who return over half of everything they order, causing 17.4 lakh rupees in losses."
    )

    # =========================================================
    # SLIDE 7: CATEGORY BENCHMARK (With Category Bar Chart!)
    # =========================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_bg(s7)
    add_header(s7, "7", "Category Performance: Best vs. Worst", "DEPARTMENT ECONOMICS")

    # Left Column: Breakdown Cards
    cat_boxes = [
        ("🏆 Electronics (Top Revenue)", "Rs. 3.19 Cr Sales  |  18.9% Return Rate  |  Rs. 67.5L Refunds", "Primary revenue anchor; returns driven by tech defects and transit damage.", COLOR_CYAN),
        ("🚨 Clothing & Apparel (Critical Problem)", "Rs. 36.3 Lakh Sales  |  34.5% Return Rate  |  Rs. 13.8L Refunds", "Worst return rate! More than 1 out of 3 garments sent back due to sizing.", COLOR_ROSE),
        ("⭐ Beauty & Personal Care (Best Retention)", "Rs. 10.8 Lakh Sales  |  11.9% Return Rate  |  Rs. 1.1L Refunds", "Lowest return rate on the platform due to strict hygiene policies.", COLOR_EMERALD),
    ]

    for i, (title, stats, note, col) in enumerate(cat_boxes):
        top = Inches(1.6 + i * 1.5)
        add_card(s7, Inches(0.8), top, Inches(6.1), Inches(1.35), col)
        tb = s7.shapes.add_textbox(Inches(1.0), top + Inches(0.08), Inches(5.7), Inches(1.15))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col

        p_st = tf.add_paragraph()
        p_st.text = stats
        p_st.font.size = Pt(11)
        p_st.font.bold = True
        p_st.font.color.rgb = COLOR_TEXT_MAIN

        p_nt = tf.add_paragraph()
        p_nt.text = note
        p_nt.font.size = Pt(10)
        p_nt.font.color.rgb = COLOR_TEXT_MUTED

    # Right Column: Category Chart Image
    add_card(s7, Inches(7.1), Inches(1.6), Inches(5.433), Inches(4.5))
    s7.shapes.add_picture(str(charts["category"]), Inches(7.2), Inches(1.8), Inches(5.2), Inches(4.0))

    add_speaker_cue(
        s7,
        "Electronics brings in the most revenue at 3.2 crore rupees. But Clothing is our biggest problem: it has an alarming 34.5% return rate, meaning more than one out of every three garments is returned."
    )

    # =========================================================
    # SLIDE 8: RETURN ROOT CAUSES (With Reasons Donut!)
    # =========================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_bg(s8)
    add_header(s8, "8", "Why Are Products Returned?", "ROOT CAUSE BREAKDOWN")

    # Left Column: Reason Details
    add_card(s8, Inches(0.8), Inches(1.6), Inches(6.3), Inches(4.5))
    tb_s8 = s8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.9), Inches(4.1))
    tf_s8 = tb_s8.text_frame
    tf_s8.word_wrap = True

    p = tf_s8.paragraphs[0]
    p.text = "🔍 Top Stated Return Drivers (1,135 Returns):"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(8)

    reasons_list = [
        ("👕 1. Size / Fit Issue (28.3% - 321 orders):", "Dominates apparel. Customers frequently order 2 sizes and return 1."),
        ("📦 2. Defective / Damaged (22.0% - 250 orders):", "Transit damage in fragile electronics and solid wood furniture."),
        ("🎨 3. Not as Described (18.1% - 205 orders):", "Color or specifications did not match the website catalog photos."),
        ("🤔 4. Changed Mind (15.4% - 175 orders):", "Impulse shopping triggered by high discounts (>20%)."),
        ("⏱️ 5. Late Delivery (16.2% - 184 orders):", "Shipments taking >5 days face high doorstep refusal rates.")
    ]
    for title, desc in reasons_list:
        p_r = tf_s8.add_paragraph()
        p_r.text = f"{title} "
        p_r.font.size = Pt(11.5)
        p_r.font.bold = True
        p_r.font.color.rgb = COLOR_TEXT_MAIN
        run = p_r.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED
        p_r.space_after = Pt(4)

    # Right Column: Donut Chart Image
    add_card(s8, Inches(7.3), Inches(1.6), Inches(5.233), Inches(4.5))
    s8.shapes.add_picture(str(charts["reasons"]), Inches(7.4), Inches(1.8), Inches(5.0), Inches(4.0))

    add_speaker_cue(
        s8,
        "Why do customers return items? The number one reason is sizing issues at 28%, followed by damaged goods during transit at 22%, and items not matching descriptions at 18%."
    )

    # =========================================================
    # SLIDE 9: PAYMENT RISK (With COD Risk Bar Chart!)
    # =========================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_bg(s9)
    add_header(s9, "9", "Hidden Risk: Cash on Delivery (COD)", "PAYMENT METHODS & TRANSIT SPEED")

    # Left Column: Insights
    add_card(s9, Inches(0.8), Inches(1.6), Inches(6.1), Inches(4.5))
    tb_s9 = s9.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.7), Inches(4.1))
    tf_s9 = tb_s9.text_frame
    tf_s9.word_wrap = True

    p = tf_s9.paragraphs[0]
    p.text = "💳 Payment Mode Impact on Returns:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_ROSE
    p.space_after = Pt(10)

    points_s9 = [
        ("💵 Cash on Delivery (COD) Risk:", "Records a 31.8% return/refusal rate. Because no money was paid upfront, customers easily refuse parcels at the doorstep."),
        ("💳 Digital Payments (UPI & Cards):", "Average return rate is only ~20%. Upfront financial commitment sharply reduces casual cancellations."),
        ("🚨 +11% Risk Premium:", "COD orders have an 11% higher return rate than prepaid orders for identical products!"),
        ("🚀 Delivery Speed Matters:", "Orders delivered within 1–2 days have a 15% return rate, compared to 26% for orders taking over 5 days.")
    ]
    for title, desc in points_s9:
        p_pt = tf_s9.add_paragraph()
        p_pt.text = f"• {title} "
        p_pt.font.size = Pt(12)
        p_pt.font.bold = True
        p_pt.font.color.rgb = COLOR_TEXT_MAIN
        run = p_pt.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED
        p_pt.space_after = Pt(6)

    # Right Column: Payment Bar Chart Image
    add_card(s9, Inches(7.1), Inches(1.6), Inches(5.433), Inches(4.5))
    s9.shapes.add_picture(str(charts["payment"]), Inches(7.2), Inches(1.8), Inches(5.2), Inches(4.0))

    add_speaker_cue(
        s9,
        "A critical finding is payment mode: Cash on Delivery has a 32% return rate compared to 20% for UPI and cards. When customers do not pay upfront, they reject packages much more easily."
    )

    # =========================================================
    # SLIDE 10: ACTION PLAN & SAVINGS (With ROI Chart!)
    # =========================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_bg(s10)
    add_header(s10, "10", "Action Plan & Strategic Solutions", "RECOVERING RS. 25 LAKHS ANNUALLY")

    # Left Column: 4 Solutions
    add_card(s10, Inches(0.8), Inches(1.6), Inches(6.1), Inches(4.5))
    tb_s10 = s10.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.7), Inches(4.1))
    tf_s10 = tb_s10.text_frame
    tf_s10.word_wrap = True

    p = tf_s10.paragraphs[0]
    p.text = "🎯 4 Strategic Business Interventions:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_after = Pt(8)

    solutions = [
        ("1. Fix Clothing Sizing:", "Implement 3D size charts, height/weight fit recommendations, and customer fit reviews to cut apparel returns by 40%."),
        ("2. Shift Away from COD:", "Offer 2% instant discounts for UPI payments, and require WhatsApp OTP verification before dispatching COD parcels."),
        ("3. Protect Fragile Products:", "Upgrade protective packaging for monitors and desks, and fast-track courier delivery under 4 days."),
        ("4. Monitor Serial Returners:", "Charge a small restocking fee for accounts with return rates over 50% to prevent return abuse.")
    ]
    for title, desc in solutions:
        p_sol = tf_s10.add_paragraph()
        p_sol.text = f"{title} "
        p_sol.font.size = Pt(11.5)
        p_sol.font.bold = True
        p_sol.font.color.rgb = COLOR_TEXT_MAIN
        run = p_sol.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED
        p_sol.space_after = Pt(5)

    # Right Column: ROI Chart Image
    add_card(s10, Inches(7.1), Inches(1.6), Inches(5.433), Inches(4.5))
    s10.shapes.add_picture(str(charts["roi"]), Inches(7.2), Inches(1.8), Inches(5.2), Inches(4.0))

    add_speaker_cue(
        s10,
        "To conclude: by improving sizing guides, encouraging UPI payments, protecting fragile packages, and monitoring serial returners, the company can cut returns by 5% and save 25 lakh rupees every year. Thank you!"
    )

    # Save to primary aesthetic presentation file
    prs.save(str(PRIMARY_FILE))
    print(f"Aesthetic presentation successfully saved to: {PRIMARY_FILE}")

    try:
        prs.save(str(SECONDARY_FILE))
        print(f"Also saved to: {SECONDARY_FILE}")
    except PermissionError:
        print(f"Note: {SECONDARY_FILE.name} is currently open in PowerPoint; saved to {PRIMARY_FILE.name}")

    return PRIMARY_FILE


if __name__ == "__main__":
    build_aesthetic_deck()
