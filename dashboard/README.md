# D2C Merchant Growth & Profitability Analytics

A data-driven analytics project designed to analyze D2C merchant performance across revenue, conversion, marketing efficiency, customer retention, and profitability.

## Business Objective

The objective is to identify growth opportunities for D2C brands by analyzing:

- Revenue and order performance
- Conversion funnel performance
- Customer retention
- Marketing efficiency
- Contribution profit and margins
- Brand-level growth opportunities

## Brands Analyzed

The project uses synthetic data representing five D2C brands:

- AuraGlow — Beauty
- UrbanThread — Fashion
- HomeNest — Home & Lifestyle
- TechEase — Electronics Accessories
- WellRoot — Wellness

> **Note:** All merchant and transaction data in this project is synthetic and created for portfolio analysis purposes.

## Analytics Workflow

Raw Data  
↓  
SQL Analysis  
↓  
Python EDA & Customer Analysis  
↓  
Power BI Dashboard  
↓  
Growth Diagnosis  
↓  
Business Recommendations

## Key Metrics

- Total Revenue
- Total Orders
- Average Order Value (AOV)
- Contribution Profit
- Contribution Margin
- Marketing Spend
- Blended ROAS
- CTR
- Conversion Rate
- Repeat Customer Rate

## Power BI Dashboard

The dashboard contains five analytical areas:

### 1. Executive Overview
Tracks overall revenue, orders, AOV, contribution profit, ROAS, and contribution margin.

### 2. Conversion Funnel
Analyzes sessions, product views, add-to-cart, checkout, purchases, and conversion rate.

### 3. Marketing & Customers
Analyzes marketing spend, impressions, clicks, CTR, customer acquisition, and repeat customers.

### 4. Profitability
Analyzes revenue, COGS, shipping costs, gross profit, contribution profit, and contribution margin.

### 5. Growth Opportunities
Compares brands across profitability, conversion, retention, and revenue to identify actionable growth opportunities.

## Technical Stack

- SQL
- Python
- Pandas
- Power BI
- DAX
- Excel/CSV
- Data Visualization
- Product & Growth Analytics

## Project Structure

```text
D2C-Merchant-Growth-Analytics/
│
├── app/
├── dashboard/
│   └── D2C-Merchant-Growth-Analytics.pbix
│
├── data/
│   ├── orders.csv
│   ├── customers.csv
│   ├── products.csv
│   ├── marketing.csv
│   └── website_funnel.csv
│
├── notebooks/
│   ├── 02_eda.py
│   └── 03_funnel_customer_analysis.py
│
├── sql/
│   ├── 01_revenue.sql
│   ├── 02_funnel.sql
│   ├── 03_marketing.sql
│   ├── 04_customer.sql
│   └── 05_profitability.sql
│
├── generate_data.py
├── requirements.txt
└── README.md