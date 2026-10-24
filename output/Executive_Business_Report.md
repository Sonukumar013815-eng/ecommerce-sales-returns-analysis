# Executive Business Report: E-Commerce Sales, Returns & Customer Analysis

**Generated Date:** 2026-10-24 14:49
**Dataset Source:** `C:\Users\lenovo\OneDrive\Desktop\project\data\ecommerce_orders_and_returns.csv` | **Analyzed Records:** 5,000
**Date Range:** 2025-01-01 to 2026-03-31

---

## 1. Executive Summary & Core KPIs

- **Gross Sales (Total Invoiced):** Rs. 49,643,272.50
- **Net Sales (Realized):** Rs. 38,527,628.00
- **Revenue Realization Rate:** 77.61% (Loss to returns: 22.39%)
- **Total Refund Loss:** Rs. 11,115,644.50
- **Total Orders Processed:** 5,000
- **Total Returned Orders:** 1,135 (22.70% Order Return Rate)
- **Total Units Sold:** 7,459
- **Active Customer Base:** 811
- **Average Order Value (Gross):** Rs. 9,928.65
- **Average Days to Return:** 8.0 days
- **Estimated Net Profit:** Rs. 10,209,535.86 (26.5% Margin)

---

## 2. Strategic Insights & Anomalies Detected

### 1. [Warning] High Overall Returns
- **Finding:** Overall order return rate is 22.7%, resulting in Rs. 11,115,644 of refunded revenue (22.4% of gross sales).
- **Recommended Business Action:** Review post-order confirmation and fit/quality guidance to reduce return velocity.

### 2. [Alert] Highest Return Category
- **Finding:** 'Clothing' exhibits the highest return rate at 34.5% (Refund loss: Rs. 1,375,875).
- **Recommended Business Action:** Target this category with enhanced visual sizing charts, customer reviews, or pre-shipping inspection.

### 3. [Critical] Cash on Delivery Return Spike
- **Finding:** COD orders experience a 31.8% return/refusal rate compared to 20.9% for prepaid methods (+10.9% gap).
- **Recommended Business Action:** Incentivize digital prepayment (UPI/Cards) via 2-5% instant cashback or require OTP verification on COD dispatches.

### 4. [Notice] Serial Returners Impact
- **Finding:** 53 customers were identified as serial returners (>=3 orders and >=50% return rate), generating Rs. 1,740,846 in return refunds.
- **Recommended Business Action:** Implement targeted return fees or require manual review on high-frequency return profiles.

### 5. [Info] Dominant Return Driver
- **Finding:** The top stated return reason is 'Size / Fit Issue', accounting for 28.3% of all returns (321 orders).
- **Recommended Business Action:** Audit product listing descriptions, dimensional accuracy, and QA checks for this failure mode.

---

## 3. Product Category & Sales Breakdown

| Category | Gross Sales | Net Sales | Refund Loss | Orders | Returns | Return Rate % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Electronics | Rs. 31,876,200 | Rs. 25,123,640 | Rs. 6,752,560 | 1,288 | 243 | **18.9%** |
| Home & Furniture | Rs. 11,009,868 | Rs. 8,580,488 | Rs. 2,429,380 | 1,068 | 224 | **21.0%** |
| Clothing | Rs. 3,630,562 | Rs. 2,254,688 | Rs. 1,375,875 | 1,343 | 463 | **34.5%** |
| Sports & Fitness | Rs. 2,046,678 | Rs. 1,603,435 | Rs. 443,242 | 638 | 126 | **19.8%** |
| Beauty & Personal Care | Rs. 1,079,965 | Rs. 965,378 | Rs. 114,587 | 663 | 79 | **11.9%** |

---

## 4. Customer Purchasing Behaviour & RFM Segmentation

- **Unique Customers:** 811
- **Repeat Purchase Rate:** 71.76%
- **Identified Serial Returners:** 53 accounts (Accountable for Rs. 1,740,846 in refunded gross sales)

| RFM Customer Segment | Customer Count | Avg Gross Spend | Avg Return Rate % | Net Revenue Contribution |
| :--- | :--- | :--- | :--- | :--- |
| Champions & VIPs | 226 | Rs. 173,426 | 20.2% | Rs. 30,566,519 |
| Loyal Customers | 178 | Rs. 33,754 | 19.4% | Rs. 4,648,924 |
| Potential Loyalists | 172 | Rs. 17,512 | 22.3% | Rs. 2,334,930 |
| At Risk / Promising | 161 | Rs. 7,382 | 20.8% | Rs. 884,424 |
| Hibernating / Inactive | 74 | Rs. 3,245 | 28.4% | Rs. 92,830 |

---

## 5. Return Root Cause Breakdown

| Stated Return Reason | Number of Returns | Share of Returns % |
| :--- | :--- | :--- |
| Size / Fit Issue | 321 | 28.3% |
| Defective / Damaged | 256 | 22.6% |
| Not as Described | 250 | 22.0% |
| Changed Mind | 142 | 12.5% |
| Late Delivery | 96 | 8.5% |
| Found Better Price | 70 | 6.2% |

---

## 6. Payment & Shipping Method Dynamics

### Payment Method Return Propensity

| Payment Method | Orders | Returned Orders | Return Rate % | Total Refunds |
| :--- | :--- | :--- | :--- | :--- |
| Cash on Delivery | 689 | 219 | **31.8%** | Rs. 1,825,630 |
| Credit Card | 1,422 | 317 | **22.3%** | Rs. 2,778,661 |
| UPI | 2,018 | 426 | **21.1%** | Rs. 4,360,378 |
| Net Banking | 264 | 54 | **20.4%** | Rs. 865,716 |
| Debit Card | 607 | 119 | **19.6%** | Rs. 1,285,260 |

*End of Executive Business Report.*
