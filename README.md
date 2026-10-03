# D2C Merchant Growth & Profitability Analytics

A portfolio project that analyzes synthetic e-commerce data across five fictional D2C brands to diagnose growth, marketing, funnel, retention, and profitability constraints.

## Business flow

Raw E-commerce Data → Python/SQL → KPI Analysis → Power BI Dashboard → Growth Diagnosis → Recommendations

## Fictional brands

- AuraGlow — Beauty
- UrbanThread — Fashion
- HomeNest — Home & Lifestyle
- TechEase — Electronics Accessories
- WellRoot — Wellness

> All brands and data in this project are synthetic and created for portfolio/learning purposes. They are not ShopDeck merchants.

## Dataset

The generator creates:
- 50,000+ orders
- 10,000+ customers
- 40 products
- 12 months of order data
- Marketing performance
- Website funnel data

Files:
- data/orders.csv
- data/customers.csv
- data/products.csv
- data/marketing.csv
- data/website_funnel.csv

## Metrics

Revenue = Quantity × Selling Price − Discount

AOV = Revenue / Orders

CAC = Marketing Spend / New Customers

ROAS = Attributed Revenue / Marketing Spend

Gross Profit = Revenue − COGS

Contribution Profit = Revenue − COGS − Marketing Cost − Shipping Cost − RTO/Return Cost

Profit Margin = Contribution Profit / Revenue

## How to run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate data

```bash
python generate_data.py
```

### 3. Run the dashboard/app

```bash
streamlit run app/app.py
```

## Project structure

D2C-Merchant-Growth-Analytics/
├── data/
├── notebooks/
├── sql/
├── dashboard/
├── app/
├── generate_data.py
├── requirements.txt
└── README.md
