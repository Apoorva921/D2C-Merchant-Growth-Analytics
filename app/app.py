import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px

st.set_page_config(page_title="D2C Merchant Growth Analytics", layout="wide")

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"

orders = pd.read_csv(DATA/"orders.csv", parse_dates=["order_date"])
marketing = pd.read_csv(DATA/"marketing.csv", parse_dates=["date"])
funnel = pd.read_csv(DATA/"website_funnel.csv", parse_dates=["date"])
customers = pd.read_csv(DATA/"customers.csv", parse_dates=["first_order_date"])

orders = orders[orders["status"] == "Delivered"].copy()

st.title("D2C Merchant Growth & Profitability Analytics")
st.caption("Synthetic portfolio dataset — fictional D2C brands")

brand = st.sidebar.selectbox("Select Brand", ["All"] + sorted(orders["brand"].unique()))

if brand != "All":
    o = orders[orders["brand"] == brand].copy()
    f = funnel[funnel["brand"] == brand].copy()
    m = marketing[marketing["brand"] == brand].copy()
else:
    o, f, m = orders.copy(), funnel.copy(), marketing.copy()

revenue = o["revenue"].sum()
order_count = o["order_id"].nunique()
aov = revenue / order_count if order_count else 0
cogs = o["cogs"].sum()
shipping = o["shipping_cost"].sum()
marketing_spend = m["ad_spend"].sum()
profit = revenue - cogs - shipping - marketing_spend
margin = profit / revenue * 100 if revenue else 0

new_customers = o["customer_id"].nunique()
cac = marketing_spend / new_customers if new_customers else 0

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Revenue", f"₹{revenue/100000:.1f}L")
col2.metric("Orders", f"{order_count:,}")
col3.metric("AOV", f"₹{aov:,.0f}")
col4.metric("CAC", f"₹{cac:,.0f}")
col5.metric("Contribution Profit", f"₹{profit/100000:.1f}L")
col6.metric("Profit Margin", f"{margin:.1f}%")

st.divider()

left, right = st.columns(2)

with left:
    monthly = o.groupby(o["order_date"].dt.to_period("M").astype(str))["revenue"].sum().reset_index()
    monthly.columns = ["month", "revenue"]
    fig = px.line(monthly, x="month", y="revenue", markers=True,
                  title="Monthly Revenue")
    st.plotly_chart(fig, use_container_width=True)

with right:
    brand_rev = orders.groupby("brand", as_index=False)["revenue"].sum()
    fig = px.bar(brand_rev, x="brand", y="revenue", title="Revenue by Brand")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Funnel")

sessions = f["sessions"].sum()
views = f["product_views"].sum()
cart = f["add_to_cart"].sum()
checkout = f["checkout"].sum()
purchases = f["purchases"].sum()

funnel_df = pd.DataFrame({
    "Stage": ["Sessions", "Product Views", "Add to Cart", "Checkout", "Purchases"],
    "Users": [sessions, views, cart, checkout, purchases]
})
fig = px.funnel(funnel_df, x="Users", y="Stage", title="E-commerce Funnel")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Growth Diagnosis")

session_conversion = purchases / sessions * 100 if sessions else 0
cart_rate = cart / views * 100 if views else 0
checkout_rate = checkout / cart * 100 if cart else 0

if session_conversion < 2.0:
    constraint = "Conversion"
    evidence = f"Session-to-purchase conversion is {session_conversion:.2f}%. Investigate product-page and checkout drop-offs."
    actions = "Test product-page messaging, mobile UX, offers and checkout friction."
elif margin < 15:
    constraint = "Profitability"
    evidence = f"Contribution margin is {margin:.1f}%. Shipping, COGS and acquisition costs should be reviewed."
    actions = "Review shipping economics, product mix, CAC and discounting."
elif cac > 900:
    constraint = "Acquisition Efficiency"
    evidence = f"CAC is ₹{cac:,.0f}. Review channel-level spend and customer acquisition efficiency."
    actions = "Shift spend toward efficient channels and test creative/audience combinations."
else:
    constraint = "Retention / Expansion"
    evidence = "Core acquisition and conversion metrics are comparatively healthy in this diagnostic."
    actions = "Focus on repeat purchase, CRM, cross-sell and high-value customer segments."

c1, c2, c3 = st.columns(3)
c1.metric("Primary Constraint", constraint)
c2.write("**Evidence**")
c2.write(evidence)
c3.write("**Recommended Action**")
c3.write(actions)

st.caption("Diagnostic outputs are portfolio analysis, not claims of real merchant performance.")
