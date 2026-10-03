import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

# Location of this Python file
NOTEBOOK_DIR = Path(__file__).resolve().parent

# Main project folder
BASE_DIR = NOTEBOOK_DIR.parent

# Data folder
DATA_DIR = BASE_DIR / "data"

# Output folder
OUTPUT_DIR = BASE_DIR / "analysis_output"

# Create output folder
OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

orders = pd.read_csv(
    DATA_DIR / "orders.csv"
)

customers = pd.read_csv(
    DATA_DIR / "customers.csv"
)

products = pd.read_csv(
    DATA_DIR / "products.csv"
)

marketing = pd.read_csv(
    DATA_DIR / "marketing.csv"
)

funnel = pd.read_csv(
    DATA_DIR / "website_funnel.csv"
)


# ============================================================
# BASIC INFORMATION
# ============================================================

print("=" * 60)
print("D2C MERCHANT GROWTH ANALYTICS - EDA")
print("=" * 60)

print("\nDATASET SHAPES")

print("Orders:", orders.shape)
print("Customers:", customers.shape)
print("Products:", products.shape)
print("Marketing:", marketing.shape)
print("Funnel:", funnel.shape)


# ============================================================
# DATA QUALITY
# ============================================================

print("\n" + "=" * 60)
print("DATA QUALITY")
print("=" * 60)

print("\nMissing values - Orders")

print(
    orders.isnull().sum()
)

print("\nDuplicate orders")

print(
    orders["order_id"].duplicated().sum()
)

print("\nDuplicate customers")

print(
    customers["customer_id"].duplicated().sum()
)

print("\nDuplicate products")

print(
    products["product_id"].duplicated().sum()
)


# ============================================================
# ORDERS ANALYSIS
# ============================================================

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)

print("\n" + "=" * 60)
print("ORDER STATUS")
print("=" * 60)

print(
    orders["status"].value_counts()
)


print("\nBRAND DISTRIBUTION")

print(
    orders["brand"].value_counts()
)


# ============================================================
# REVENUE
# ============================================================

delivered_orders = orders[
    orders["status"] == "Delivered"
].copy()


total_revenue = (
    delivered_orders["revenue"].sum()
)


total_orders = (
    delivered_orders["order_id"].nunique()
)


aov = (
    total_revenue /
    total_orders
)


print("\n" + "=" * 60)
print("CORE BUSINESS METRICS")
print("=" * 60)

print(
    f"Total Revenue: ₹{total_revenue:,.2f}"
)

print(
    f"Delivered Orders: {total_orders:,}"
)

print(
    f"Average Order Value: ₹{aov:,.2f}"
)


# ============================================================
# REVENUE BY BRAND
# ============================================================

brand_revenue = (
    delivered_orders
    .groupby("brand")["revenue"]
    .sum()
    .sort_values(
        ascending=False
    )
)

print("\nREVENUE BY BRAND")

print(
    brand_revenue
)


# ============================================================
# MONTHLY REVENUE
# ============================================================

delivered_orders["month"] = (
    delivered_orders["order_date"]
    .dt.to_period("M")
    .astype(str)
)


monthly_revenue = (
    delivered_orders
    .groupby("month")["revenue"]
    .sum()
)


print("\nMONTHLY REVENUE")

print(
    monthly_revenue
)


# ============================================================
# PROFITABILITY
# ============================================================

delivered_orders["gross_profit"] = (
    delivered_orders["revenue"]
    -
    delivered_orders["cogs"]
)


delivered_orders[
    "contribution_profit"
] = (
    delivered_orders["revenue"]
    -
    delivered_orders["cogs"]
    -
    delivered_orders["shipping_cost"]
)


brand_profitability = (
    delivered_orders
    .groupby("brand")
    .agg(

        revenue=(
            "revenue",
            "sum"
        ),

        cogs=(
            "cogs",
            "sum"
        ),

        shipping=(
            "shipping_cost",
            "sum"
        ),

        gross_profit=(
            "gross_profit",
            "sum"
        ),

        contribution_profit=(
            "contribution_profit",
            "sum"
        )
    )
)


brand_profitability[
    "profit_margin"
] = (
    brand_profitability[
        "contribution_profit"
    ]
    /
    brand_profitability[
        "revenue"
    ]
    *
    100
)


print("\nBRAND PROFITABILITY")

print(
    brand_profitability.round(2)
)


# ============================================================
# CUSTOMER ANALYSIS
# ============================================================

customer_orders = (
    delivered_orders
    .groupby("customer_id")
    .agg(

        orders=(
            "order_id",
            "count"
        ),

        revenue=(
            "revenue",
            "sum"
        )
    )
)


print("\nCUSTOMER ANALYSIS")

print(
    customer_orders.describe()
)


# ============================================================
# NEW VS REPEAT CUSTOMERS
# ============================================================

customer_order_counts = (
    delivered_orders
    .groupby("customer_id")
    .size()
)


new_customers = (
    customer_order_counts == 1
).sum()


repeat_customers = (
    customer_order_counts > 1
).sum()


print(
    f"\nNew Customers: {new_customers:,}"
)

print(
    f"Repeat Customers: {repeat_customers:,}"
)


# ============================================================
# SAVE ANALYTICS DATA
# ============================================================

brand_revenue.to_csv(
    OUTPUT_DIR /
    "brand_revenue.csv"
)


monthly_revenue.to_csv(
    OUTPUT_DIR /
    "monthly_revenue.csv"
)


brand_profitability.to_csv(
    OUTPUT_DIR /
    "brand_profitability.csv"
)


customer_orders.to_csv(
    OUTPUT_DIR /
    "customer_analysis.csv"
)


# ============================================================
# CHART 1 — REVENUE BY BRAND
# ============================================================

plt.figure(
    figsize=(10, 6)
)

brand_revenue.plot(
    kind="bar"
)

plt.title(
    "Revenue by D2C Brand"
)

plt.xlabel(
    "Brand"
)

plt.ylabel(
    "Revenue (₹)"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()


plt.savefig(
    OUTPUT_DIR /
    "revenue_by_brand.png"
)

plt.close()


# ============================================================
# CHART 2 — MONTHLY REVENUE
# ============================================================

plt.figure(
    figsize=(12, 6)
)

monthly_revenue.plot()

plt.title(
    "Monthly Revenue Trend"
)

plt.xlabel(
    "Month"
)

plt.ylabel(
    "Revenue (₹)"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()


plt.savefig(
    OUTPUT_DIR /
    "monthly_revenue.png"
)

plt.close()


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 60)
print("EDA COMPLETE")
print("=" * 60)

print(
    f"\nOutput saved to:\n{OUTPUT_DIR}"
)