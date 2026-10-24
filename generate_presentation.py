"""
Generate 10 Executive Presentation Slides for the
E-Commerce Sales, Returns, and Customer Analysis Project
(Kaggle — E-Commerce Dataset Order and Return)
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "E_Commerce_Sales_Returns_Customer_Analysis.pptx"


def build_presentation(output_path=OUTPUT_FILE):
    prs = Presentation()
    # 16:9 widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Executive Theme Palette (Modern Midnight Navy & Premium Accents)
    COLOR_BG = RGBColor(15, 23, 42)          # #0F172A Deep Navy
    COLOR_CARD = RGBColor(30, 41, 59)        # #1E293B Slate Card
    COLOR_BORDER = RGBColor(71, 85, 105)     # #475569 Slate Border
    COLOR_ACCENT = RGBColor(99, 102, 241)    # #6366F1 Electric Indigo
    COLOR_EMERALD = RGBColor(16, 185, 129)   # #10B981 Emerald
    COLOR_ROSE = RGBColor(239, 68, 68)       # #EF4444 Rose Red (Returns)
    COLOR_AMBER = RGBColor(245, 158, 11)     # #F59E0B Amber
    COLOR_CYAN = RGBColor(6, 182, 212)       # #06B6D4 Cyan
    COLOR_WHITE = RGBColor(248, 250, 252)    # #F8FAFC Pure White
    COLOR_MUTED = RGBColor(148, 163, 184)    # #94A3B8 Secondary Muted

    def apply_slide_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_tag="E-COMMERCE COMMERCIAL INTELLIGENCE"):
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(10), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = category_tag.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_ACCENT

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.7))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_BORDER
        line.line.fill.background()

    def add_card(slide, left, top, width, height, border_color=COLOR_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        return card

    # =========================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s1)

    add_card(s1, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1), COLOR_ACCENT)
    tb = s1.shapes.add_textbox(Inches(2.0), Inches(1.8), Inches(9.333), Inches(3.9))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "KAGGLE E-COMMERCE BENCHMARK ANALYSIS • EXECUTIVE DECK"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_ACCENT
    p0.space_after = Pt(14)

    p1 = tf.add_paragraph()
    p1.text = "E-Commerce Sales, Returns &\nCustomer Behaviour Analysis"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.space_after = Pt(16)

    p2 = tf.add_paragraph()
    p2.text = "Root-Cause Return Diagnostics, Customer RFM Segmentation, Net Realization & Growth Strategy"
    p2.font.size = Pt(15)
    p2.font.color.rgb = COLOR_MUTED
    p2.space_after = Pt(24)

    p3 = tf.add_paragraph()
    p3.text = "Prepared for Executive Leadership, Merchandising, Supply Chain & Analytics Teams • 10-Slide Brief"
    p3.font.size = Pt(12)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_EMERALD

    # =========================================================
    # SLIDE 2: PROBLEM STATEMENT, CONTEXT & OBJECTIVES
    # =========================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s2)
    add_header(s2, "Problem Statement, Context & Business Objectives", "PROJECT FOUNDATION")

    cards_s2 = [
        ("The Real-World Scenario", "An e-commerce enterprise handles thousands of transactions across multiple product categories. While top-line sales grow, product returns cause severe revenue leakage, inventory holding costs, and customer churn.", COLOR_ACCENT),
        ("Why The Problem Matters", "Gross sales figures mask profitability. A 22.7% return rate erodes over 22% of revenue. Understanding return patterns across products, customers, and payment methods reveals vital margin differences.", COLOR_ROSE),
        ("Target Stakeholders", "Built for E-Commerce Analysts, Sales & Merchandising Managers, Customer Retention Teams, and Business Decision-Makers to formulate data-backed operational interventions.", COLOR_CYAN),
        ("Core Deliverable", "An end-to-end data analytics pipeline, dynamic interactive dashboard, automated anomaly detector, and actionable strategic roadmap supported by empirical data.", COLOR_EMERALD)
    ]

    for i, (heading, text, border_col) in enumerate(cards_s2):
        col_idx = i % 2
        row_idx = i // 2
        left = Inches(0.8 + col_idx * 5.95)
        top = Inches(1.8 + row_idx * 2.65)
        
        add_card(s2, left, top, Inches(5.75), Inches(2.4), border_col)
        tb = s2.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), Inches(5.35), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = heading
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = border_col
        p.space_after = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = text
        p2.font.size = Pt(13)
        p2.font.color.rgb = COLOR_MUTED

    # =========================================================
    # SLIDE 3: DATASET ARCHITECTURE & QUALITY PIPELINE
    # =========================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s3)
    add_header(s3, "Dataset Architecture & Data Quality Pipeline", "ENGINEERING & VALIDATION")

    steps = [
        ("1. Data Structure", "5,000 orders across 811 customers with 31 relational attributes covering order dates, demographics, SKUs, pricing, payments, and returns."),
        ("2. Validation & Quality", "Parsed and validated timestamps (Order/Return dates), enforced numeric bounds (Quantity >= 1, Price >= 0), and removed duplicate transactions."),
        ("3. Handling Missingness", "Zero-loss imputation: non-returned records assigned 'Not Applicable', categorical fields standardized, text casing aligned."),
        ("4. Derived Measures", "Calculated Net Realized Sales, Refund Loss, Revenue Realization %, Order Return %, Customer Return Frequency, and RFM scores.")
    ]

    for i, (title, desc) in enumerate(steps):
        left = Inches(0.8 + i * 2.98)
        add_card(s3, left, Inches(1.8), Inches(2.8), Inches(4.9), COLOR_ACCENT)
        tb = s3.shapes.add_textbox(left + Inches(0.18), Inches(2.0), Inches(2.44), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(12)

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = COLOR_MUTED

    # =========================================================
    # SLIDE 4: EXECUTIVE COMMERCIAL REVIEW & CORE FINANCIAL KPIS
    # =========================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s4)
    add_header(s4, "Executive Commercial Review & Core Financial KPIs", "HIGH-LEVEL PERFORMANCE")

    kpis_s4 = [
        ("Rs. 4.96 Cr", "Gross Invoiced Sales", "5,000 Orders Processed", COLOR_ACCENT),
        ("Rs. 3.85 Cr", "Net Realized Sales", "77.61% Revenue Realization", COLOR_EMERALD),
        ("22.70%", "Order Return Rate", "1,135 Returned Orders", COLOR_ROSE),
        ("Rs. 1.11 Cr", "Refund Revenue Loss", "22.39% Direct Margin Erosion", COLOR_AMBER)
    ]

    for i, (val, label, sub, color) in enumerate(kpis_s4):
        left = Inches(0.8 + i * 2.98)
        add_card(s4, left, Inches(1.8), Inches(2.8), Inches(1.8), color)
        tb = s4.shapes.add_textbox(left + Inches(0.15), Inches(1.9), Inches(2.5), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = label.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_MUTED

        p_val = tf.add_paragraph()
        p_val.text = val
        p_val.font.size = Pt(26)
        p_val.font.bold = True
        p_val.font.color.rgb = COLOR_WHITE

        p_sub = tf.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(10)
        p_sub.font.color.rgb = color

    # Narrative Summary Card
    add_card(s4, Inches(0.8), Inches(3.9), Inches(11.733), Inches(2.9))
    tb_narr = s4.shapes.add_textbox(Inches(1.1), Inches(4.1), Inches(11.1), Inches(2.5))
    tf_narr = tb_narr.text_frame
    tf_narr.word_wrap = True

    pn = tf_narr.paragraphs[0]
    pn.text = "Key Financial Highlights & Realization Analysis"
    pn.font.size = Pt(16)
    pn.font.bold = True
    pn.font.color.rgb = COLOR_WHITE
    pn.space_after = Pt(10)

    points_s4 = [
        ("Top-Line Strength vs. Bottom-Line Leakage", "The platform achieved robust gross turnover of Rs. 4.96 Cr; however, Rs. 1.11 Cr was refunded, representing substantial operational cost and tied-up working capital."),
        ("Average Order Value (AOV)", "Gross AOV stands at Rs. 9,928 across 7,459 total units sold. Net realized AOV remains consistent at Rs. 9,968, indicating returns affect high- and low-value transactions alike."),
        ("Realized Net Profit", "Estimated net profit reached Rs. 1.02 Cr (26.5% margin), reflecting sound unit economics dampened primarily by reverse-logistics overhead.")
    ]
    for title, desc in points_s4:
        p = tf_narr.add_paragraph()
        p.text = f"•  {title}: {desc}"
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(6)

    # =========================================================
    # SLIDE 5: SALES PERFORMANCE & MONTHLY REVENUE VELOCITY
    # =========================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s5)
    add_header(s5, "Sales Velocity & Regional Revenue Distribution", "SALES TRAJECTORY")

    col_l = add_card(s5, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.0))
    tb_l = s5.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.6))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    pl = tf_l.paragraphs[0]
    pl.text = "Monthly Sales & Realization Dynamics"
    pl.font.size = Pt(16)
    pl.font.bold = True
    pl.font.color.rgb = COLOR_CYAN
    pl.space_after = Pt(8)

    monthly_bulletins = [
        ("Steady Monthly Baseline", "Averaged Rs. 33 Lakhs in gross sales monthly, demonstrating resilient market demand."),
        ("Q4 Holiday Surge (Oct-Dec)", "Seasonal spike with sales exceeding Rs. 38 Lakhs monthly, driven by festival promotions and consumer gifting."),
        ("Post-Holiday Return Lag", "January-February reflected a sharp uptick in return volume (reaching 24.5%), trailing the Q4 order influx."),
        ("Revenue Retention Stability", "Net revenue realization hovered reliably between 75% and 80% across all 15 analyzed months.")
    ]
    for title, desc in monthly_bulletins:
        p = tf_l.add_paragraph()
        p.text = f"•  {title}: {desc}"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(6)

    col_r = add_card(s5, Inches(6.8), Inches(1.8), Inches(5.75), Inches(5.0))
    tb_r = s5.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.35), Inches(4.6))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    pr = tf_r.paragraphs[0]
    pr.text = "Geographic Market Performance"
    pr.font.size = Pt(16)
    pr.font.bold = True
    pr.font.color.rgb = COLOR_EMERALD
    pr.space_after = Pt(8)

    regions = [
        ("West Zone (Mumbai, Pune, Ahmedabad)", "Rs. 1.35 Cr Gross | 21.8% Return Rate", "Largest revenue contributor, high tech & lifestyle penetration."),
        ("North Zone (Delhi, Jaipur, Lucknow)", "Rs. 1.28 Cr Gross | 23.4% Return Rate", "High COD utilization, strong volume in winter clothing."),
        ("South Zone (Bengaluru, Chennai, Hyderabad)", "Rs. 1.24 Cr Gross | 21.2% Return Rate", "Highest prepaid adoption, lowest return friction."),
        ("East Zone (Kolkata, Patna, Bhubaneswar)", "Rs. 1.09 Cr Gross | 24.6% Return Rate", "Longer transit times correlating with higher customer return initiation.")
    ]
    for name, stat, desc in regions:
        p1 = tf_r.add_paragraph()
        p1.text = f"•  {name}"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_WHITE
        p2 = tf_r.add_paragraph()
        p2.text = f"   {stat} — {desc}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_MUTED
        p2.space_after = Pt(4)

    # =========================================================
    # SLIDE 6: CUSTOMER PURCHASING BEHAVIOUR & RFM ANALYSIS
    # =========================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s6)
    add_header(s6, "Customer Purchasing Behaviour & RFM Segmentation", "CUSTOMER INSIGHTS")

    cust_kpis = [
        ("811", "Active Customers", "Total Unique Buyer Base", COLOR_ACCENT),
        ("84.0%", "Repeat Purchase Rate", "Strong Loyalty Foundation", COLOR_EMERALD),
        ("6.17", "Orders per Customer", "High Platform Engagement", COLOR_CYAN),
        ("53", "Serial Returners Flagged", ">=3 Orders & >=50% Returns", COLOR_ROSE)
    ]
    for i, (val, label, sub, color) in enumerate(cust_kpis):
        left = Inches(0.8 + i * 2.98)
        add_card(s6, left, Inches(1.8), Inches(2.8), Inches(1.6), color)
        tb = s6.shapes.add_textbox(left + Inches(0.15), Inches(1.85), Inches(2.5), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = label.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_MUTED

        p_val = tf.add_paragraph()
        p_val.text = val
        p_val.font.size = Pt(24)
        p_val.font.bold = True
        p_val.font.color.rgb = COLOR_WHITE

        p_sub = tf.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(9)
        p_sub.font.color.rgb = color

    # RFM Segment Details
    add_card(s6, Inches(0.8), Inches(3.6), Inches(11.733), Inches(3.2))
    tb_rfm = s6.shapes.add_textbox(Inches(1.0), Inches(3.75), Inches(11.3), Inches(2.9))
    tf_rfm = tb_rfm.text_frame
    tf_rfm.word_wrap = True

    prfm = tf_rfm.paragraphs[0]
    prfm.text = "RFM Segmentation & The Serial Returner Anomaly"
    prfm.font.size = Pt(16)
    prfm.font.bold = True
    prfm.font.color.rgb = COLOR_WHITE
    prfm.space_after = Pt(8)

    rfm_points = [
        ("Champions & VIPs (~25% of buyers)", "Generate 38% of net revenue with an average spend of Rs. 72,000 and an exemplary low return rate of 14.2%."),
        ("Loyal & Potential Loyalists (~45% of buyers)", "Reliable reorder cadence across furniture and electronics; responsive to seasonal discounts with moderate return rate (~20%)."),
        ("Serial Returners Alert (53 Customer Accounts)", "Disproportionately high-frequency returners accountable for Rs. 17.4 Lakh in gross refunds. Approximately 6.5% of accounts generate ~16% of all return volume."),
        ("Actionable Strategic Policy", "Implement progressive restocking fees, soft-gating on COD orders, or dedicated customer concierge support for high-return profiles.")
    ]
    for title, desc in rfm_points:
        p = tf_rfm.add_paragraph()
        p.text = f"•  {title}: {desc}"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(5)

    # =========================================================
    # SLIDE 7: PRODUCT & DEPARTMENT PERFORMANCE MATRIX
    # =========================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s7)
    add_header(s7, "Product & Department Performance Matrix", "CATEGORY ECONOMICS")

    categories = [
        ("Electronics", "Rs. 3.19 Cr", "Rs. 2.51 Cr", "18.9%", "Rs. 67.5 L", "Anchor Category; high ticket value", COLOR_ACCENT),
        ("Home & Furniture", "Rs. 1.10 Cr", "Rs. 85.8 L", "21.0%", "Rs. 24.3 L", "Bulky shipments; transit damage risk", COLOR_CYAN),
        ("Clothing & Apparel", "Rs. 36.3 L", "Rs. 22.5 L", "34.5%", "Rs. 13.8 L", "CRITICAL RISK; severe sizing return rate", COLOR_ROSE),
        ("Sports & Fitness", "Rs. 20.5 L", "Rs. 16.0 L", "19.8%", "Rs. 4.4 L", "Steady performance, minimal wear returns", COLOR_EMERALD),
        ("Beauty & Personal Care", "Rs. 10.8 L", "Rs. 9.7 L", "11.9%", "Rs. 1.1 L", "Best-in-class retention due to hygiene policies", COLOR_AMBER),
    ]

    for i, (cat, gross, net, ret_rate, refund, notes, col) in enumerate(categories):
        top = Inches(1.8 + i * 1.0)
        add_card(s7, Inches(0.8), top, Inches(11.733), Inches(0.88), col)
        
        tb = s7.shapes.add_textbox(Inches(1.0), top + Inches(0.08), Inches(11.3), Inches(0.72))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"{cat.upper()}  |  Gross: {gross}  •  Net: {net}  •  Refunds: {refund}  •  Return Rate: {ret_rate}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

        p2 = tf.add_paragraph()
        p2.text = f"Diagnostic: {notes}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_MUTED

    # Bottom takeaway
    add_card(s7, Inches(0.8), Inches(6.1), Inches(11.733), Inches(0.75))
    tb_b = s7.shapes.add_textbox(Inches(1.0), Inches(6.15), Inches(11.3), Inches(0.65))
    tf_b = tb_b.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "Key Insight: Clothing represents only 7.3% of gross turnover but accounts for over 40% of all return volume (34.5% return rate)."
    p_b.font.size = Pt(12)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_ROSE

    # =========================================================
    # SLIDE 8: RETURN BEHAVIOUR & ROOT CAUSE ANALYSIS
    # =========================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s8)
    add_header(s8, "Return Behaviour & Root Cause Deep-Dive", "REVERSE LOGISTICS")

    reasons = [
        ("Size / Fit Issue", "28.3%", "321 Orders", "Primary apparel driver. High disparity between customer expectations and actual fit.", COLOR_ROSE),
        ("Defective / Damaged", "22.0%", "250 Orders", "Prominent in Electronics & Furniture. Reflects packaging and courier transit strain.", COLOR_AMBER),
        ("Not as Described", "18.1%", "205 Orders", "Color inaccuracies, missing specification clarity on product listing pages.", COLOR_CYAN),
        ("Changed Mind", "15.4%", "175 Orders", "Impulse buying fueled by steep discounts (>20%) with zero buyer friction.", COLOR_MUTED),
        ("Late Delivery / Other", "16.2%", "184 Orders", "Shipments taking >5 days experience 2.2x higher cancellation & return rates.", COLOR_BORDER),
    ]

    for i, (reason, share, count, explanation, col) in enumerate(reasons):
        left = Inches(0.8 + i * 2.38)
        add_card(s8, left, Inches(1.8), Inches(2.25), Inches(4.9), col)
        tb = s8.shapes.add_textbox(left + Inches(0.12), Inches(1.95), Inches(2.0), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = reason
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(6)

        p_s = tf.add_paragraph()
        p_s.text = share
        p_s.font.size = Pt(24)
        p_s.font.bold = True
        p_s.font.color.rgb = col

        p_c = tf.add_paragraph()
        p_c.text = count
        p_c.font.size = Pt(11)
        p_c.font.color.rgb = COLOR_MUTED
        p_c.space_after = Pt(10)

        p_e = tf.add_paragraph()
        p_e.text = explanation
        p_e.font.size = Pt(11)
        p_e.font.color.rgb = COLOR_MUTED

    # =========================================================
    # SLIDE 9: TRANSACTION RISK: PAYMENT METHODS & TRANSIT SPEED
    # =========================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s9)
    add_header(s9, "Transaction Risk: Payment Methods & Shipping Speed", "RISK CORRELATIONS")

    col_pm = add_card(s9, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.0))
    tb_pm = s9.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.6))
    tf_pm = tb_pm.text_frame
    tf_pm.word_wrap = True

    ppm = tf_pm.paragraphs[0]
    ppm.text = "Payment Method Risk Comparison"
    ppm.font.size = Pt(16)
    ppm.font.bold = True
    ppm.font.color.rgb = COLOR_ROSE
    ppm.space_after = Pt(10)

    pm_stats = [
        ("Cash on Delivery (COD)", "31.8% Return Rate", "Zero financial commitment at checkout results in casual ordering and doorstep refusal."),
        ("Credit / Debit Cards", "20.4% Return Rate", "Prepaid commitment significantly reduces frivolous rejections."),
        ("UPI / Digital Wallets", "19.6% Return Rate", "Fastest growing, lowest return rate among all major payment modes."),
        ("Key Gap Analysis", "+10.9% Risk Premium", "Direct return risk premium incurred on COD transactions compared to prepaid payment modes.")
    ]
    for title, rate, desc in pm_stats:
        p1 = tf_pm.add_paragraph()
        p1.text = f"•  {title} — {rate}"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_WHITE
        p2 = tf_pm.add_paragraph()
        p2.text = f"   {desc}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_MUTED
        p2.space_after = Pt(6)

    col_sh = add_card(s9, Inches(6.8), Inches(1.8), Inches(5.75), Inches(5.0))
    tb_sh = s9.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.35), Inches(4.6))
    tf_sh = tb_sh.text_frame
    tf_sh.word_wrap = True

    psh = tf_sh.paragraphs[0]
    psh.text = "Shipping Velocity & Discount Impact"
    psh.font.size = Pt(16)
    psh.font.bold = True
    psh.font.color.rgb = COLOR_AMBER
    psh.space_after = Pt(10)

    sh_stats = [
        ("Same-Day / Next-Day Delivery", "15.2% Return Rate", "High purchase intent; immediate gratification minimizes buyer remorse."),
        ("Standard Ground (4-7 Days)", "25.8% Return Rate", "Delivery delays directly correlate with increased return propensity."),
        ("Steep Discount Tiers (>20%)", "26.4% Return Rate", "Deep discounts attract price-sensitive, low-intent buyers prone to return."),
        ("Average Days to Return", "8.0 Days Mean Duration", "Most returns initiated within 4-10 days of physical delivery.")
    ]
    for title, rate, desc in sh_stats:
        p1 = tf_sh.add_paragraph()
        p1.text = f"•  {title} — {rate}"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_WHITE
        p2 = tf_sh.add_paragraph()
        p2.text = f"   {desc}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_MUTED
        p2.space_after = Pt(6)

    # =========================================================
    # SLIDE 10: STRATEGIC ROADMAP & ACTIONABLE INTERVENTIONS
    # =========================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s10)
    add_header(s10, "Strategic Roadmap & Operational Interventions", "EXECUTIVE ACTION PLAN")

    pillars = [
        ("1. Merchandising & Sizing", [
            "Implement standardized 3D visual sizing guides for Apparel & Footwear.",
            "Display customer fit ratings ('Runs True to Size / Runs Small') on PDPs.",
            "Enrich high-return electronics listings with unboxing video demonstrations."
        ], COLOR_ACCENT),
        ("2. Payment & Checkout", [
            "Incentivize UPI/Prepaid transactions with 2-3% instant cashback.",
            "Implement mandatory WhatsApp/SMS OTP confirmation for COD orders >Rs. 2,000.",
            "Restrict COD access for customer profiles with proven return rates >50%."
        ], COLOR_EMERALD),
        ("3. Logistics & Operations", [
            "Reinforce transit packaging on fragile furniture and monitor displays.",
            "Fast-track deliveries to stay under the 4-day threshold to cut buyer remorse.",
            "Establish dedicated reverse-logistics QA to recover 15% in restocking efficiency."
        ], COLOR_CYAN)
    ]

    for i, (title, points_list, col) in enumerate(pillars):
        left = Inches(0.8 + i * 3.98)
        add_card(s10, left, Inches(1.8), Inches(3.8), Inches(4.2), col)
        tb = s10.shapes.add_textbox(left + Inches(0.18), Inches(1.95), Inches(3.44), Inches(3.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(10)

        for pt in points_list:
            p_bullet = tf.add_paragraph()
            p_bullet.text = f"• {pt}"
            p_bullet.font.size = Pt(12)
            p_bullet.font.color.rgb = COLOR_MUTED
            p_bullet.space_after = Pt(6)

    # ROI Projection Banner
    add_card(s10, Inches(0.8), Inches(6.15), Inches(11.733), Inches(0.8), COLOR_EMERALD)
    tb_roi = s10.shapes.add_textbox(Inches(1.0), Inches(6.2), Inches(11.3), Inches(0.7))
    tf_roi = tb_roi.text_frame
    p_roi = tf_roi.paragraphs[0]
    p_roi.text = "TARGET BUSINESS IMPACT: Achieving a 5.0% reduction in platform return rate (from 22.7% to 17.7%) recovers approximately Rs. 25 Lakhs in retained margin annually."
    p_roi.font.size = Pt(12)
    p_roi.font.bold = True
    p_roi.font.color.rgb = COLOR_EMERALD

    prs.save(str(output_path))
    print(f"Presentation deck successfully created at: {output_path}")
    return output_path


if __name__ == "__main__":
    build_presentation()
