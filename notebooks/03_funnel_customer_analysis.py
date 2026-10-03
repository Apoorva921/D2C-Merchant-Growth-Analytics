import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

NOTEBOOK_DIR = Path(__file__).resolve().parent
BASE_DIR = NOTEBOOK_DIR.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "analysis_output"

OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

funnel = pd.read_csv(
    DATA_DIR / "website_funnel.csv"
)

customers = pd.read_csv(
    DATA_DIR / "customers.csv"
)

orders = pd.read_csv(
    DATA_DIR / "orders.csv"
)


# ============================================================
# CONVERT DATES
# ============================================================

funnel["date"] = pd.to_datetime(
    funnel["date"]
)

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)


# ============================================================
# FUNNEL TOTALS
# ============================================================

funnel_totals = funnel[
    [
        "sessions",
        "product_views",
        "add_to_cart",
        "checkout",
        "purchases"
    ]
].sum()


print("=" * 60)
print("D2C MERCHANT GROWTH ANALYTICS")
print("FUNNEL & CUSTOMER ANALYSIS")
print("=" * 60)


print("\nTOTAL FUNNEL")

print(funnel_totals)


# ============================================================
# FUNNEL CONVERSION RATES
# ============================================================

sessions = funnel_totals["sessions"]
product_views = funnel_totals["product_views"]
add_to_cart = funnel_totals["add_to_cart"]
checkout = funnel_totals["checkout"]
purchases = funnel_totals["purchases"]


view_rate = (
    product_views / sessions * 100
)

cart_rate = (
    add_to_cart / product_views * 100
)

checkout_rate = (
    checkout / add_to_cart * 100
)

purchase_rate = (
    purchases / checkout * 100
)

overall_conversion = (
    purchases / sessions * 100
)


print("\n" + "=" * 60)
print("FUNNEL CONVERSION RATES")
print("=" * 60)

print(
    f"Session → Product View: {view_rate:.2f}%"
)

print(
    f"Product View → Add to Cart: {cart_rate:.2f}%"
)

print(
    f"Add to Cart → Checkout: {checkout_rate:.2f}%"
)

print(
    f"Checkout → Purchase: {purchase_rate:.2f}%"
)

print(
    f"Overall Conversion: {overall_conversion:.2f}%"
)


# ============================================================
# BRAND LEVEL FUNNEL
# ============================================================

brand_funnel = (
    funnel
    .groupby("brand")
    .agg(
        sessions=("sessions", "sum"),
        product_views=("product_views", "sum"),
        add_to_cart=("add_to_cart", "sum"),
        checkout=("checkout", "sum"),
        purchases=("purchases", "sum")
    )
)


brand_funnel["view_rate"] = (
    brand_funnel["product_views"]
    /
    brand_funnel["sessions"]
    * 100
)


brand_funnel["cart_rate"] = (
    brand_funnel["add_to_cart"]
    /
    brand_funnel["product_views"]
    * 100
)


brand_funnel["checkout_rate"] = (
    brand_funnel["checkout"]
    /
    brand_funnel["add_to_cart"]
    * 100
)


brand_funnel["purchase_rate"] = (
    brand_funnel["purchases"]
    /
    brand_funnel["checkout"]
    * 100
)


brand_funnel["overall_conversion"] = (
    brand_funnel["purchases"]
    /
    brand_funnel["sessions"]
    * 100
)


print("\n" + "=" * 60)
print("BRAND FUNNEL PERFORMANCE")
print("=" * 60)

print(
    brand_funnel.round(2)
)


# ============================================================
# FIND BRAND WITH LOWEST CONVERSION
# ============================================================

lowest_conversion_brand = (
    brand_funnel["overall_conversion"]
    .idxmin()
)

highest_conversion_brand = (
    brand_funnel["overall_conversion"]
    .idxmax()
)


print(
    f"\nLowest conversion brand: "
    f"{lowest_conversion_brand}"
)

print(
    f"Highest conversion brand: "
    f"{highest_conversion_brand}"
)


# ============================================================
# CUSTOMER ORDER ANALYSIS
# ============================================================

orders_delivered = orders[
    orders["status"] == "Delivered"
].copy()


customer_summary = (
    orders_delivered
    .groupby("customer_id")
    .agg(
        order_count=("order_id", "count"),
        revenue=("revenue", "sum")
    )
)


# ============================================================
# CUSTOMER TYPE
# ============================================================

customer_summary["customer_type"] = np.where(
    customer_summary["order_count"] > 1,
    "Repeat",
    "New"
)


print("\n" + "=" * 60)
print("CUSTOMER TYPE")
print("=" * 60)

print(
    customer_summary["customer_type"]
    .value_counts()
)


# ============================================================
# CUSTOMER SEGMENT SUMMARY
# ============================================================

customer_segments = (
    customer_summary
    .groupby("customer_type")
    .agg(
        customers=("order_count", "count"),
        orders=("order_count", "sum"),
        revenue=("revenue", "sum")
    )
)


customer_segments["revenue_per_customer"] = (
    customer_segments["revenue"]
    /
    customer_segments["customers"]
)


print("\nCUSTOMER SEGMENTS")

print(
    customer_segments.round(2)
)


# ============================================================
# REPEAT PURCHASE RATE
# ============================================================

total_customers = len(
    customer_summary
)

repeat_customers = (
    customer_summary[
        customer_summary["order_count"] > 1
    ].shape[0]
)


repeat_purchase_rate = (
    repeat_customers
    /
    total_customers
    * 100
)


print(
    f"\nRepeat Purchase Rate: "
    f"{repeat_purchase_rate:.2f}%"
)


# ============================================================
# ORDERS PER CUSTOMER
# ============================================================

average_orders_per_customer = (
    customer_summary["order_count"].mean()
)


print(
    f"Average Orders per Customer: "
    f"{average_orders_per_customer:.2f}"
)


# ============================================================
# CUSTOMER REVENUE DISTRIBUTION
# ============================================================

print("\nCUSTOMER REVENUE STATISTICS")

print(
    customer_summary["revenue"].describe()
)


# ============================================================
# SAVE OUTPUTS
# ============================================================

funnel_summary = pd.DataFrame({
    "metric": [
        "Sessions",
        "Product Views",
        "Add to Cart",
        "Checkout",
        "Purchases"
    ],
    "value": [
        sessions,
        product_views,
        add_to_cart,
        checkout,
        purchases
    ]
})


funnel_summary.to_csv(
    OUTPUT_DIR / "funnel_summary.csv",
    index=False
)


brand_funnel.to_csv(
    OUTPUT_DIR / "brand_funnel.csv"
)


customer_segments.to_csv(
    OUTPUT_DIR / "customer_segments.csv"
)


customer_summary.to_csv(
    OUTPUT_DIR / "customer_summary.csv"
)


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 60)
print("FUNNEL & CUSTOMER ANALYSIS COMPLETE")
print("=" * 60)

print(
    f"\nOutput saved to:\n{OUTPUT_DIR}"
)