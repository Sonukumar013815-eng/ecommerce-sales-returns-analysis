# E-Commerce Sales, Returns, and Customer Analysis
### Kaggle — E-Commerce Dataset Order and Return

An end-to-end data analytics, machine-learning-ready pipeline, business intelligence dashboard, and executive presentation suite designed to analyze sales performance, customer purchasing behaviour, and product return patterns.

---

## 📌 1. Problem Statement & Business Context

An e-commerce enterprise handles historical order, customer, product, and return transactions:
- **Real-World Scenario:** Product returns create severe operational drag, reverse logistics costs, and revenue leakage. Gross invoiced sales figures conceal substantial margin erosion.
- **Why It Matters:** Return patterns reveal fundamental differences across product categories (e.g. apparel sizing vs electronic defects), payment methods (Cash on Delivery vs prepaid), customer cohorts (serial returners), and delivery speed.
- **Target Audience:** E-commerce analysts, sales & merchandising teams, customer care leads, and executive decision-makers.
- **Expected Outcome:** A comprehensive data cleaning and analytics engine, an interactive multi-tab dashboard, automated anomaly alerts, an executive markdown business report, and an executive 10-slide PowerPoint presentation deck (`.pptx`).

---

## 🚀 2. What Was Built & Key Features

### A. Data Engineering & Transformation Pipeline
- **Schema & Architecture:** Ingests and standardizes 5,000 order transactions across 811 customers with 31 relational features spanning 15 months.
- **Data Validation:** Strict timestamp parsing (`Order_Date`, `Return_Date`), boundary enforcement (`Quantity` $\ge 1$, `Unit_Price` $\ge 0$), and automated transaction deduplication.
- **Missing Value Handling:** Zero-loss imputation; non-returned orders classified as "Not Applicable", categorical features standardized.
- **Derived Measures:**
  - `Gross Sales` (Total Invoiced Revenue)
  - `Net Sales` (Realized Revenue retained after returns)
  - `Refund Loss` (Direct revenue erosion)
  - `Revenue Realization Rate %` (`Net Sales / Gross Sales`)
  - `Order Return Rate %` and `Sales Return Rate %`
  - `Days to Return` (physical delivery to return initiation)
  - `Discount Tiers` and `Price Tiers`

### B. Customer Purchasing Behaviour & RFM Segmentation
- **Repeat Purchase Dynamics:** 811 active customers with an **84% Repeat Purchase Rate** (average 6.17 orders per customer).
- **RFM Segmentation:** Algorithmic scoring based on **Recency**, **Frequency**, and **Monetary Value** into Champions & VIPs, Loyal Customers, Potential Loyalists, At Risk, and Hibernating.
- **Serial Returners Watchlist:** Flags customer accounts with $\ge 3$ orders and $\ge 50\%$ return rates (53 identified accounts responsible for **Rs. 17.4 Lakh** in refunds).

### C. Product & Department Performance Matrix
- **Category Economics:**
  - **Electronics:** Rs. 3.19 Cr gross | 18.9% return rate | Rs. 67.5 Lakh refund loss.
  - **Home & Furniture:** Rs. 1.10 Cr gross | 21.0% return rate | Rs. 24.3 Lakh refund loss.
  - **Clothing & Apparel:** Rs. 36.3 Lakh gross | **34.5% return rate** | Rs. 13.8 Lakh refund loss.
  - **Sports & Fitness:** Rs. 20.5 Lakh gross | 19.8% return rate | Rs. 4.4 Lakh refund loss.
  - **Beauty & Personal Care:** Rs. 10.8 Lakh gross | **11.9% return rate** | Rs. 1.1 Lakh refund loss.
- **Star vs. Troublemaker Matrix:** Bubble chart evaluating sales volume against return propensity.
- **Top 10 Best Sellers:** Realized net sales ranking after deducting returns.

### D. Return Behaviour & Root Cause Deep-Dive
- **Return Drivers:**
  - **Size / Fit Issue (28.3%):** Dominates apparel returns (50% of clothing returns).
  - **Defective / Damaged (22.0%):** Major driver for fragile electronics and furniture.
  - **Not as Described (18.1%):** Product listing specification mismatch.
  - **Changed Mind (15.4%):** Impulse purchases tied to steep discounts (>20%).
  - **Late Delivery (16.2%):** Transit delays (>5 days) lead to doorstep refusals.
- **Payment Method Risk:** Cash on Delivery (COD) records a **31.8%** return rate vs **20.9%** for prepaid UPI/cards (+10.9% return gap).
- **Days-to-Return Distribution:** Mean return initiation of **8.0 days**.

### E. Interactive 7-Tab Streamlit Dashboard
1. **📊 Executive Overview:** Revenue realization bar chart, return rate trend line, core KPI cards.
2. **📈 Sales Performance:** Regional pie charts, sub-category treemap, weekly/monthly velocity.
3. **👥 Customer Purchasing Behaviour:** RFM distribution, order frequency, spend vs return scatter.
4. **📦 Product & Category Analytics:** Product portfolio bubble chart, top 10 net sales table.
5. **🔄 Return Behaviour & Root Cause:** Return reasons donut chart, COD impact bar chart, days-to-return histogram.
6. **🚨 Strategic Insights & Anomalies:** Algorithmic alert badges and operational roadmap.
7. **📋 Data Explorer & Export:** Searchable transaction explorer with instant CSV download.

### F. Executive 10-Slide Presentation Deck (`.pptx`)
A widescreen 16:9 PowerPoint presentation generated using `python-pptx` with midnight navy styling, cards, and executive insights:
- **Slide 1:** Title Slide & Project Scope
- **Slide 2:** Problem Statement, Context & Business Objectives
- **Slide 3:** Dataset Architecture & Data Quality Pipeline
- **Slide 4:** Executive Commercial Review & Core Financial KPIs
- **Slide 5:** Sales Velocity & Regional Revenue Distribution
- **Slide 6:** Customer Purchasing Behaviour & RFM Segmentation
- **Slide 7:** Product & Department Performance Matrix
- **Slide 8:** Return Behaviour & Root Cause Deep-Dive
- **Slide 9:** Transaction Risk: Payment Methods & Shipping Speed
- **Slide 10:** Strategic Roadmap & Operational Interventions

---

## 🛠️ 3. Project File Structure

```
project/
├── data/
│   └── ecommerce_orders_and_returns.csv             # Kaggle-standard 5,000-order dataset
├── output/
│   ├── Executive_Business_Report.md                 # Formal executive markdown report
│   ├── monthly_sales_comparison.png                 # Publication-quality chart
│   ├── category_return_rates.png                    # Category return rate chart
│   ├── monthly_sales_trend.csv                      # Monthly sales & return summary
│   ├── category_performance.csv                     # Category performance summary
│   ├── customer_rfm_segments.csv                    # Customer RFM breakdown
│   ├── return_reasons_summary.csv                   # Return reasons distribution
│   ├── returns_by_payment_method.csv                # Payment method return rates
│   └── insights.json                                # Automated anomaly alerts
├── E_Commerce_Sales_Returns_Customer_Analysis.pptx   # Executive 10-Slide Deck (Dark Cards)
├── Simple_Easy_Present_Ecommerce_Analysis.pptx      # Simple 10-Slide Deck with Speaking Cues
├── Aesthetic_Ecommerce_Presentation.pptx            # Aesthetic 10-Slide Deck with Embedded Charts & Icons
├── create_aesthetic_presentation.py                 # Aesthetic Presentation Generator
├── generate_simple_presentation.py                  # Simple Presentation Generator
├── generate_presentation.py                         # Standard Presentation Generator
├── analysis.py                                      # Data cleaning, KPI, and analytics pipeline
├── dashboard.py                                     # Interactive 7-tab Streamlit dashboard
├── app.py                                           # Streamlit app wrapper
├── generate_dataset.py                              # Kaggle benchmark dataset generator
├── requirements.txt                                 # Project dependencies
└── README.md                                        # Documentation
```

---

## 📦 4. Setup & How to Run

### 1. Requirements
Ensure you have **Python 3.10** or higher installed.

### 2. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 3. Run Analytics Pipeline & Generate Reports
```bash
python analysis.py
```

### 4. Generate the 10-Slide Presentation Deck
```bash
python generate_presentation.py
```
*Creates `E_Commerce_Sales_Returns_Customer_Analysis.pptx` in the project folder.*

### 5. Launch the Interactive Dashboard
```bash
python -m streamlit run dashboard.py
```
*Open your browser at `http://localhost:8501`.*
