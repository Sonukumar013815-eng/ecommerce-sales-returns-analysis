"""
Generate a Clean, Simple, Easy-to-Present 10-Slide Presentation Deck
for the E-Commerce Sales, Returns, and Customer Analysis Project.

Designed specifically so students and analysts can present effortlessly:
- Big, readable text and clear numbers
- Simple 3-4 bullet points per slide (no clutter)
- Built-in 'What to Say' presentation cues on every slide
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "Simple_Easy_Present_Ecommerce_Analysis.pptx"
MAIN_PPTX = BASE_DIR / "E_Commerce_Sales_Returns_Customer_Analysis.pptx"


def build_simple_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Clean, High-Contrast Modern Theme
    # Light executive background with crisp dark cards or dark navy with crisp readable cards
    COLOR_BG = RGBColor(248, 250, 252)          # Clean Off-White #F8FAFC
    COLOR_CARD = RGBColor(255, 255, 255)       # Crisp White Card #FFFFFF
    COLOR_BORDER = RGBColor(226, 232, 240)     # Subtle Slate Border #E2E8F0
    COLOR_TEXT_MAIN = RGBColor(15, 23, 42)     # Deep Charcoal #0F172A
    COLOR_TEXT_MUTED = RGBColor(71, 85, 105)   # Slate Muted #475569
    
    # Accent Colors
    COLOR_PRIMARY = RGBColor(37, 99, 235)      # Royal Blue #2563EB
    COLOR_SUCCESS = RGBColor(16, 185, 129)     # Emerald Green #10B981
    COLOR_DANGER = RGBColor(225, 29, 72)       # Rose Red #E11D48
    COLOR_AMBER = RGBColor(217, 119, 6)        # Amber #D97706
    COLOR_PURPLE = RGBColor(124, 58, 237)      # Violet #7C3AED
    COLOR_CUE_BG = RGBColor(241, 245, 249)     # Soft Cue Box #F1F5F9

    def apply_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, slide_num, title, subtitle):
        # Slide number & tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.3))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = f"SLIDE {slide_num} OF 10  •  E-COMMERCE DATA ANALYSIS"
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_PRIMARY

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.6))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MAIN

        # Subtitle
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(0.35))
        tf_sub = sub_box.text_frame
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED

    def add_white_card(slide, left, top, width, height, border_color=COLOR_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        return card

    def add_speaking_cue(slide, cue_text):
        """Adds a simple 'What to Say' box at the bottom for easy presenting."""
        cue_card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.3), Inches(11.733), Inches(0.85)
        )
        cue_card.fill.solid()
        cue_card.fill.fore_color.rgb = COLOR_CUE_BG
        cue_card.line.color.rgb = COLOR_PRIMARY
        cue_card.line.width = Pt(1.2)

        tb = slide.shapes.add_textbox(Inches(1.0), Inches(6.32), Inches(11.3), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = "🗣️ What to Say: "
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY

        run = p.add_run()
        run.text = f'"{cue_text}"'
        run.font.size = Pt(11)
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================
    # SLIDE 1: TITLE SLIDE (Simple & Confident)
    # =========================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_bg(s1)

    # Large Center Card
    add_white_card(s1, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5), COLOR_PRIMARY)
    
    tb1 = s1.shapes.add_textbox(Inches(1.8), Inches(1.6), Inches(9.7), Inches(4.3))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "PROJECT PRESENTATION • DATA ANALYTICS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(12)

    p_t = tf1.add_paragraph()
    p_t.text = "E-Commerce Sales, Returns &\nCustomer Behaviour Analysis"
    p_t.font.size = Pt(36)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_TEXT_MAIN
    p_t.space_after = Pt(14)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Understanding What Sells, Who Buys, and Why Products Get Returned"
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = COLOR_TEXT_MUTED
    p_sub.space_after = Pt(24)

    p_meta = tf1.add_paragraph()
    p_meta.text = "Dataset: Kaggle E-Commerce Orders & Returns  •  Tools: Python, Pandas, Streamlit"
    p_meta.font.size = Pt(13)
    p_meta.font.bold = True
    p_meta.font.color.rgb = COLOR_SUCCESS

    # =========================================================
    # SLIDE 2: PROJECT OVERVIEW (What & Why)
    # =========================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_bg(s2)
    add_header(s2, "2", "Project Overview & Problem Statement", "What is this project about and why does it matter?")

    cards_s2 = [
        ("The Business Problem", "The e-commerce company makes strong sales, but product returns are eating away its profits. High gross revenue looks great, but high return rates cause severe revenue loss and extra courier costs.", COLOR_PRIMARY),
        ("Why It Matters", "Returns cost money. If 22% of orders are returned, the company wastes delivery costs, restocking fees, and loses customer trust. We need to find the root causes to protect profit margins.", COLOR_DANGER),
        ("Our Core Objectives", "1. Clean and validate 5,000 transaction records\n2. Track sales performance and monthly trends\n3. Study customer loyalty and buying habits\n4. Uncover the real reasons why items get returned", COLOR_SUCCESS)
    ]

    for i, (title, body, col) in enumerate(cards_s2):
        left = Inches(0.8 + i * 3.98)
        add_white_card(s2, left, Inches(1.8), Inches(3.8), Inches(4.3), col)
        
        tb = s2.shapes.add_textbox(left + Inches(0.2), Inches(2.0), Inches(3.4), Inches(3.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(12)

        p_b = tf.add_paragraph()
        p_b.text = body
        p_b.font.size = Pt(13)
        p_b.font.color.rgb = COLOR_TEXT_MAIN

    add_speaking_cue(
        s2,
        "Good morning everyone. In this project, we analyzed an e-commerce platform to understand where the company makes its revenue and where it loses money due to customer returns."
    )

    # =========================================================
    # SLIDE 3: THE DATASET AT A GLANCE
    # =========================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_bg(s3)
    add_header(s3, "3", "The Dataset at a Glance", "Understanding the order, customer, and return records")

    stats_s3 = [
        ("5,000", "Total Transactions", "Covering 15 months of orders", COLOR_PRIMARY),
        ("811", "Unique Customers", "Across 20 Indian cities", COLOR_PURPLE),
        ("31", "Columns / Features", "Orders, customers, returns", COLOR_AMBER),
        ("100%", "Data Cleaned", "0 duplicates, valid dates", COLOR_SUCCESS)
    ]

    for i, (num, label, desc, col) in enumerate(stats_s3):
        left = Inches(0.8 + i * 2.98)
        add_white_card(s3, left, Inches(1.8), Inches(2.8), Inches(1.6), col)
        tb = s3.shapes.add_textbox(left + Inches(0.15), Inches(1.9), Inches(2.5), Inches(1.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = num
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = col

        p_lbl = tf.add_paragraph()
        p_lbl.text = label
        p_lbl.font.size = Pt(12)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = COLOR_TEXT_MAIN

        p_sub = tf.add_paragraph()
        p_sub.text = desc
        p_sub.font.size = Pt(10)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED

    # Bottom Explanation Card
    add_white_card(s3, Inches(0.8), Inches(3.6), Inches(11.733), Inches(2.5))
    tb_exp = s3.shapes.add_textbox(Inches(1.1), Inches(3.8), Inches(11.1), Inches(2.1))
    tf_exp = tb_exp.text_frame
    tf_exp.word_wrap = True

    p_e = tf_exp.paragraphs[0]
    p_e.text = "How We Prepared and Cleaned the Data:"
    p_e.font.size = Pt(16)
    p_e.font.bold = True
    p_e.font.color.rgb = COLOR_PRIMARY
    p_e.space_after = Pt(8)

    points_s3 = [
        "Date Validation: Formatted Order Date and Return Date; calculated exact delivery and return turnaround times.",
        "Missing Value Treatment: Cleaned records with missing details; marked non-returned orders clearly as 'Completed'.",
        "Deduplication: Checked for repeated Order IDs to guarantee transaction uniqueness.",
        "Derived Metrics: Created Net Realized Sales, Return Rate %, Refund Amount, and Customer RFM scores."
    ]
    for pt in points_s3:
        p_pt = tf_exp.add_paragraph()
        p_pt.text = f"•  {pt}"
        p_pt.font.size = Pt(12)
        p_pt.font.color.rgb = COLOR_TEXT_MAIN
        p_pt.space_after = Pt(3)

    add_speaking_cue(
        s3,
        "Our dataset consists of 5,000 orders placed by 811 customers. We cleaned the data by validating all dates, removing duplicates, and calculating net sales after returns."
    )

    # =========================================================
    # SLIDE 4: THE BIG NUMBERS (Executive KPIs)
    # =========================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_bg(s4)
    add_header(s4, "4", "Key Performance Indicators (The Big Numbers)", "Top-level sales, realized revenue, and return metrics")

    kpis_s4 = [
        ("Rs. 4.96 Cr", "Gross Invoiced Sales", "Total value of all orders", COLOR_PRIMARY),
        ("Rs. 3.85 Cr", "Net Realized Sales", "Money actually retained", COLOR_SUCCESS),
        ("22.7%", "Order Return Rate", "1,135 orders sent back", COLOR_DANGER),
        ("Rs. 1.11 Cr", "Lost to Refunds", "22.4% direct revenue loss", COLOR_AMBER)
    ]

    for i, (val, label, sub, color) in enumerate(kpis_s4):
        left = Inches(0.8 + i * 2.98)
        add_white_card(s4, left, Inches(1.8), Inches(2.8), Inches(1.8), color)
        tb = s4.shapes.add_textbox(left + Inches(0.15), Inches(1.9), Inches(2.5), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = label.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MUTED

        p_val = tf.add_paragraph()
        p_val.text = val
        p_val.font.size = Pt(26)
        p_val.font.bold = True
        p_val.font.color.rgb = color

        p_sub = tf.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = COLOR_TEXT_MAIN

    # Explanatory card
    add_white_card(s4, Inches(0.8), Inches(3.8), Inches(11.733), Inches(2.3))
    tb_kpi = s4.shapes.add_textbox(Inches(1.1), Inches(3.95), Inches(11.1), Inches(2.0))
    tf_kpi = tb_kpi.text_frame
    tf_kpi.word_wrap = True

    p_k = tf_kpi.paragraphs[0]
    p_k.text = "Key Takeaways from the Numbers:"
    p_k.font.size = Pt(16)
    p_k.font.bold = True
    p_k.font.color.rgb = COLOR_TEXT_MAIN
    p_k.space_after = Pt(8)

    kpi_notes = [
        "Nearly 1 out of every 4 orders (22.7%) is returned by customers.",
        "While the business recorded Rs. 4.96 Crore in sales, only Rs. 3.85 Crore was retained as actual cash.",
        "Over 1.11 Crore Rupees was given back as customer refunds — representing massive profit leakage.",
        "The Average Order Value (AOV) is Rs. 9,928, showing strong basket size despite high returns."
    ]
    for n in kpi_notes:
        p_n = tf_kpi.add_paragraph()
        p_n.text = f"•  {n}"
        p_n.font.size = Pt(13)
        p_n.font.color.rgb = COLOR_TEXT_MUTED
        p_n.space_after = Pt(4)

    add_speaking_cue(
        s4,
        "Here are the headline figures: Out of nearly 5 crore rupees in gross sales, over 1.1 crore was refunded because 22.7% of orders were returned. That is nearly 1 in every 4 orders."
    )

    # =========================================================
    # SLIDE 5: SALES PERFORMANCE & TIMELINE
    # =========================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_bg(s5)
    add_header(s5, "5", "Sales Performance & Trends", "When do customers buy and where are they located?")

    col1 = add_white_card(s5, Inches(0.8), Inches(1.8), Inches(5.75), Inches(4.3), COLOR_PRIMARY)
    tb_s1 = s5.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(3.9))
    tf_s1 = tb_s1.text_frame
    tf_s1.word_wrap = True

    p = tf_s1.paragraphs[0]
    p.text = "Monthly Sales Velocity"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    bullets_s5_1 = [
        "Steady Baseline: Monthly sales average Rs. 33 Lakhs reliably.",
        "Festival Peak (Oct - Dec): Sales surged over Rs. 38 Lakhs per month due to festival discounts and gift buying.",
        "The January Hangover: Returns spiked in January right after the heavy holiday shopping season (reaching 24.5%).",
        "Consistent Realization: Across all months, the company consistently retained about 77% of gross sales."
    ]
    for b in bullets_s5_1:
        pb = tf_s1.add_paragraph()
        pb.text = f"•  {b}"
        pb.font.size = Pt(12)
        pb.font.color.rgb = COLOR_TEXT_MAIN
        pb.space_after = Pt(6)

    col2 = add_white_card(s5, Inches(6.8), Inches(1.8), Inches(5.75), Inches(4.3), COLOR_SUCCESS)
    tb_s2 = s5.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.35), Inches(3.9))
    tf_s2 = tb_s2.text_frame
    tf_s2.word_wrap = True

    p = tf_s2.paragraphs[0]
    p.text = "Geographic Distribution"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUCCESS
    p.space_after = Pt(10)

    bullets_s5_2 = [
        "West Region (27% of Sales): Mumbai, Pune, Ahmedabad lead in total electronics and gadgets revenue.",
        "North Region (26% of Sales): Delhi NCR and Jaipur lead in fashion and home goods volume.",
        "South Region (25% of Sales): Bengaluru and Hyderabad exhibit the highest prepaid adoption and lowest returns (21%).",
        "East Region (22% of Sales): Kolkata and Patna; slower delivery times correlate with higher return rates (24.6%)."
    ]
    for b in bullets_s5_2:
        pb = tf_s2.add_paragraph()
        pb.text = f"•  {b}"
        pb.font.size = Pt(12)
        pb.font.color.rgb = COLOR_TEXT_MAIN
        pb.space_after = Pt(6)

    add_speaking_cue(
        s5,
        "Looking at sales trends, business was strong year-round with a big spike in Q4 during festival sales. Geographically, demand is well-balanced across West, North, South, and East India."
    )

    # =========================================================
    # SLIDE 6: CUSTOMER PURCHASING BEHAVIOUR & RFM
    # =========================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_bg(s6)
    add_header(s6, "6", "Customer Purchasing Behaviour", "Who are the customers and who returns the most?")

    cust_metrics = [
        ("811", "Total Buyers", "Active Customer Pool", COLOR_PRIMARY),
        ("84.0%", "Repeat Purchase Rate", "High Customer Loyalty", COLOR_SUCCESS),
        ("6.2", "Orders / Customer", "Average Purchases", COLOR_AMBER),
        ("53", "Serial Returners", "Over 50% Return Rate", COLOR_DANGER)
    ]
    for i, (val, label, sub, color) in enumerate(cust_metrics):
        left = Inches(0.8 + i * 2.98)
        add_white_card(s6, left, Inches(1.8), Inches(2.8), Inches(1.6), color)
        tb = s6.shapes.add_textbox(left + Inches(0.15), Inches(1.9), Inches(2.5), Inches(1.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = val
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = color

        p_lbl = tf.add_paragraph()
        p_lbl.text = label
        p_lbl.font.size = Pt(11)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = COLOR_TEXT_MAIN

        p_sub = tf.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(10)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED

    add_white_card(s6, Inches(0.8), Inches(3.6), Inches(11.733), Inches(2.5))
    tb_c = s6.shapes.add_textbox(Inches(1.1), Inches(3.8), Inches(11.1), Inches(2.1))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    pc = tf_c.paragraphs[0]
    pc.text = "Customer Loyalty vs. Return Abuse Discovery:"
    pc.font.size = Pt(16)
    pc.font.bold = True
    pc.font.color.rgb = COLOR_TEXT_MAIN
    pc.space_after = Pt(8)

    cust_bullets = [
        "Strong Loyalty: 84% of customers buy repeatedly, proving strong product appeal and brand trust.",
        "Top VIP Customers (25%): Generate 38% of platform revenue with a very low return rate of only 14%.",
        "⚠️ The 'Serial Returners' Discovery: We identified 53 customer accounts who ordered at least 3 times and returned MORE than 50% of everything they bought.",
        "Financial Impact: These 53 serial returners caused Rs. 17.4 Lakhs in refunds — accounting for nearly 16% of all return losses!"
    ]
    for b in cust_bullets:
        pb = tf_c.add_paragraph()
        pb.text = f"•  {b}"
        pb.font.size = Pt(13)
        pb.font.color.rgb = COLOR_TEXT_MUTED
        pb.space_after = Pt(4)

    add_speaking_cue(
        s6,
        "Most customers are loyal with an 84% repeat rate. However, we found a small group of 53 'serial returners' who return over half of what they buy, causing 17.4 lakh rupees in losses."
    )

    # =========================================================
    # SLIDE 7: CATEGORY PERFORMANCE (Best vs Worst)
    # =========================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_bg(s7)
    add_header(s7, "7", "Category Performance: Best vs. Worst", "Which product departments make profit and which cause trouble?")

    cat_rows = [
        ("Electronics", "Rs. 3.19 Cr", "18.9%", "Rs. 67.5 L", "🏆 Biggest Revenue Driver (Laptops, TVs, Headphones)", COLOR_PRIMARY),
        ("Home & Furniture", "Rs. 1.10 Cr", "21.0%", "Rs. 24.3 L", "📦 Heavy Items (Desks, Chairs, Bookshelves)", COLOR_PURPLE),
        ("Clothing & Apparel", "Rs. 36.3 Lakh", "34.5%", "Rs. 13.8 L", "🚨 CRITICAL PROBLEM: Over 1 in 3 items returned!", COLOR_DANGER),
        ("Sports & Fitness", "Rs. 20.5 Lakh", "19.8%", "Rs. 4.4 L", "🏃 Stable niche (Yoga mats, Dumbbells, Gear)", COLOR_AMBER),
        ("Beauty & Personal Care", "Rs. 10.8 Lakh", "11.9%", "Rs. 1.1 L", "⭐ Lowest Return Rate (Strict hygiene rules)", COLOR_SUCCESS),
    ]

    for i, (cat, sales, rate, loss, note, col) in enumerate(cat_rows):
        top = Inches(1.8 + i * 0.86)
        add_white_card(s7, Inches(0.8), top, Inches(11.733), Inches(0.76), col)
        
        tb = s7.shapes.add_textbox(Inches(1.0), top + Inches(0.08), Inches(11.3), Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"{cat}  —  Gross Sales: {sales}  |  Return Rate: {rate}  |  Refund Loss: {loss}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = note
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    add_speaking_cue(
        s7,
        "Electronics brings in the highest revenue at 3.2 crore rupees. But Clothing is our biggest problem area: it has an alarming 34.5% return rate, meaning more than one out of every three garments is sent back."
    )

    # =========================================================
    # SLIDE 8: WHY ARE PRODUCTS RETURNED? (Root Causes)
    # =========================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_bg(s8)
    add_header(s8, "8", "Why Are Products Returned?", "Breaking down the real root causes behind 1,135 returns")

    reasons_s8 = [
        ("Size / Fit Issue", "28.3%", "321 Orders", "Apparel & footwear sizing confusion. Customers buy two sizes and return one.", COLOR_DANGER),
        ("Defective / Damaged", "22.0%", "250 Orders", "Broken during transit or faulty electronics. Highlights packaging issues.", COLOR_AMBER),
        ("Not as Described", "18.1%", "205 Orders", "Color or specifications did not match website listing photos.", COLOR_PURPLE),
        ("Changed Mind", "15.4%", "175 Orders", "Impulse buying caused by big discounts; zero barrier to return.", COLOR_PRIMARY),
        ("Late Delivery", "16.2%", "184 Orders", "Took over 5 days; customer bought elsewhere or rejected delivery.", COLOR_TEXT_MUTED),
    ]

    for i, (reason, pct, count, desc, col) in enumerate(reasons_s8):
        left = Inches(0.8 + i * 2.38)
        add_white_card(s8, left, Inches(1.8), Inches(2.25), Inches(4.3), col)
        tb = s8.shapes.add_textbox(left + Inches(0.12), Inches(1.95), Inches(2.0), Inches(3.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = reason
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(4)

        p_pct = tf.add_paragraph()
        p_pct.text = pct
        p_pct.font.size = Pt(24)
        p_pct.font.bold = True
        p_pct.font.color.rgb = col

        p_cnt = tf.add_paragraph()
        p_cnt.text = count
        p_cnt.font.size = Pt(11)
        p_cnt.font.color.rgb = COLOR_TEXT_MUTED
        p_cnt.space_after = Pt(8)

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = COLOR_TEXT_MAIN

    add_speaking_cue(
        s8,
        "Why do customers return products? Number one is sizing issues at 28%, followed by damaged goods at 22%, and products not matching descriptions at 18%."
    )

    # =========================================================
    # SLIDE 9: THE PAYMENT RISK (COD vs Prepaid)
    # =========================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_bg(s9)
    add_header(s9, "9", "Hidden Risk: Cash on Delivery (COD)", "How payment method and delivery speed impact return rates")

    c1 = add_white_card(s9, Inches(0.8), Inches(1.8), Inches(5.75), Inches(4.3), COLOR_DANGER)
    tb_p1 = s9.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(3.9))
    tf_p1 = tb_p1.text_frame
    tf_p1.word_wrap = True

    p = tf_p1.paragraphs[0]
    p.text = "Payment Method Comparison"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_DANGER
    p.space_after = Pt(8)

    p_stats = [
        ("Cash on Delivery (COD):", "31.8% Return Rate", "Zero financial commitment at checkout makes it easy for buyers to reject parcels at their doorstep."),
        ("Credit & Debit Cards:", "20.4% Return Rate", "Customers who pay upfront rarely cancel or refuse deliveries."),
        ("UPI / Digital Wallets:", "19.6% Return Rate", "Lowest return rate and fastest growing payment method."),
        ("The Big Insight:", "+11% Return Gap", "COD orders have an 11% higher return rate for identical products!")
    ]
    for title, badge, desc in p_stats:
        pb = tf_p1.add_paragraph()
        pb.text = f"•  {title} "
        pb.font.size = Pt(12)
        pb.font.bold = True
        pb.font.color.rgb = COLOR_TEXT_MAIN
        run_b = pb.add_run()
        run_b.text = f"[{badge}] "
        run_b.font.color.rgb = COLOR_DANGER
        run_b.font.bold = True
        run_d = pb.add_run()
        run_d.text = desc
        run_d.font.bold = False
        run_d.font.color.rgb = COLOR_TEXT_MUTED
        pb.space_after = Pt(4)

    c2 = add_white_card(s9, Inches(6.8), Inches(1.8), Inches(5.75), Inches(4.3), COLOR_AMBER)
    tb_p2 = s9.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.35), Inches(3.9))
    tf_p2 = tb_p2.text_frame
    tf_p2.word_wrap = True

    p = tf_p2.paragraphs[0]
    p.text = "Delivery Speed & Discount Effects"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    p.space_after = Pt(8)

    d_stats = [
        ("Fast Delivery (1-2 Days):", "15.2% Return Rate", "Instant gratification keeps excitement high and reduces buyer remorse."),
        ("Slow Delivery (5+ Days):", "25.8% Return Rate", "Delays give buyers time to change their minds or buy elsewhere."),
        ("Heavy Discounts (>20%):", "26.4% Return Rate", "Steep sales attract impulse buyers who often return."),
        ("Average Return Time:", "8 Days", "Most returns happen within 8 days of parcel delivery.")
    ]
    for title, badge, desc in d_stats:
        pb = tf_p2.add_paragraph()
        pb.text = f"•  {title} "
        pb.font.size = Pt(12)
        pb.font.bold = True
        pb.font.color.rgb = COLOR_TEXT_MAIN
        run_b = pb.add_run()
        run_b.text = f"[{badge}] "
        run_b.font.color.rgb = COLOR_AMBER
        run_b.font.bold = True
        run_d = pb.add_run()
        run_d.text = desc
        run_d.font.bold = False
        run_d.font.color.rgb = COLOR_TEXT_MUTED
        pb.space_after = Pt(4)

    add_speaking_cue(
        s9,
        "Here is a key finding: Cash on Delivery has a 32% return rate compared to 20% for UPI and Cards. When people don't pay upfront, they reject packages much more easily."
    )

    # =========================================================
    # SLIDE 10: ACTION PLAN & RECOMMENDATIONS (Simple Solutions)
    # =========================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_bg(s10)
    add_header(s10, "10", "Action Plan & Strategic Solutions", "4 simple steps to reduce returns and save money")

    recs_s10 = [
        ("1. Fix Clothing Sizing", "Add accurate 3D size charts, height/weight fit recommendations, and customer fit feedback ('Runs true to size') to slash fashion returns by 40%.", COLOR_PRIMARY),
        ("2. Cut COD Return Rates", "Give a 2% instant discount for paying via UPI, and send a WhatsApp OTP verification before dispatching COD packages.", COLOR_SUCCESS),
        ("3. Protect Fragile Goods", "Improve packaging with bubble wrap and corner protectors for monitors and furniture, and keep delivery under 4 days.", COLOR_AMBER),
        ("4. Handle Serial Returners", "Charge a modest return shipping fee for customers with return rates above 50% to stop return abuse.", COLOR_PURPLE)
    ]

    for i, (title, body, col) in enumerate(recs_s10):
        left = Inches(0.8 + (i % 2) * 5.95)
        top = Inches(1.8 + (i // 2) * 2.15)
        add_white_card(s10, left, top, Inches(5.75), Inches(1.95), col)

        tb = s10.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(5.35), Inches(1.65))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)

        p_b = tf.add_paragraph()
        p_b.text = body
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = COLOR_TEXT_MAIN

    add_speaking_cue(
        s10,
        "To conclude: by improving size guides, encouraging UPI payments, protecting fragile packages, and monitoring serial returners, the company can cut returns by 5% and save 25 lakh rupees every year. Thank you!"
    )

    # Save to primary output file
    prs.save(str(OUTPUT_FILE))
    print(f"Presentation saved successfully to: {OUTPUT_FILE}")

    try:
        prs.save(str(MAIN_PPTX))
        print(f"Also updated: {MAIN_PPTX}")
    except PermissionError:
        print(f"Note: {MAIN_PPTX.name} is currently open in PowerPoint. Please view: {OUTPUT_FILE.name}")

    return OUTPUT_FILE


if __name__ == "__main__":
    build_simple_presentation()
