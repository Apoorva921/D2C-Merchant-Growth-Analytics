import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# 1. BASIC SETUP
# ============================================================

np.random.seed(42)

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"

# Create data folder if it does not exist
DATA.mkdir(exist_ok=True)

N_ORDERS = 55000
N_CUSTOMERS = 12000


# ============================================================
# 2. D2C BRANDS
# ============================================================

brands = {
    "AuraGlow": {
        "category": "Beauty",
        "price": 900,
        "margin": 0.58,
        "shipping": 65
    },

    "UrbanThread": {
        "category": "Fashion",
        "price": 1500,
        "margin": 0.42,
        "shipping": 95
    },

    "HomeNest": {
        "category": "Home & Lifestyle",
        "price": 1800,
        "margin": 0.36,
        "shipping": 180
    },

    "TechEase": {
        "category": "Electronics Accessories",
        "price": 1300,
        "margin": 0.25,
        "shipping": 80
    },

    "WellRoot": {
        "category": "Wellness",
        "price": 1100,
        "margin": 0.55,
        "shipping": 70
    }
}

brand_names = list(brands.keys())


# ============================================================
# 3. MARKETING CHANNELS
# ============================================================

channels = [
    "Meta Ads",
    "Google Ads",
    "Organic",
    "Influencer",
    "Email"
]


# ============================================================
# 4. ORDER STATUSES
# ============================================================

statuses = [
    "Delivered",
    "Cancelled",
    "RTO"
]


# ============================================================
# 5. DATE RANGE
# ============================================================

start = pd.Timestamp("2025-01-01")
end = pd.Timestamp("2025-12-31")

dates = pd.date_range(
    start=start,
    end=end,
    freq="D"
)


# ============================================================
# 6. PRODUCTS DATASET
# ============================================================

product_rows = []

pid = 1

for brand, info in brands.items():

    for i in range(8):

        selling_price = (
            info["price"] *
            np.random.uniform(0.75, 1.25)
        )

        cost_price = (
            selling_price *
            (1 - info["margin"])
        )

        product_rows.append({

            "product_id": f"P{pid:03d}",

            "brand": brand,

            "product_name":
                f"{brand} Product {i + 1}",

            "category":
                info["category"],

            "cost_price":
                round(cost_price, 2),

            "selling_price":
                round(selling_price, 2)
        })

        pid += 1


products = pd.DataFrame(product_rows)


products.to_csv(
    DATA / "products.csv",
    index=False
)


# ============================================================
# 7. CUSTOMERS DATASET
# ============================================================

customer_first_dates = pd.to_datetime(
    np.random.choice(
        dates,
        N_CUSTOMERS
    )
)


customers = pd.DataFrame({

    "customer_id": [
        f"C{i:05d}"
        for i in range(1, N_CUSTOMERS + 1)
    ],

    "first_order_date":
        customer_first_dates,

    "city":
        np.random.choice(
            [
                "Delhi",
                "Mumbai",
                "Bangalore",
                "Hyderabad",
                "Pune",
                "Gurgaon",
                "Chennai",
                "Kolkata",
                "Ahmedabad",
                "Jaipur"
            ],
            N_CUSTOMERS
        ),

    "state":
        np.random.choice(
            [
                "Delhi",
                "Maharashtra",
                "Karnataka",
                "Telangana",
                "Haryana",
                "Tamil Nadu",
                "West Bengal",
                "Gujarat",
                "Rajasthan"
            ],
            N_CUSTOMERS
        ),

    "acquisition_channel":
        np.random.choice(
            channels,
            N_CUSTOMERS,
            p=[0.30, 0.22, 0.22, 0.14, 0.12]
        )
})


customers.to_csv(
    DATA / "customers.csv",
    index=False
)


# ============================================================
# 8. ORDERS DATASET
# ============================================================

customer_ids = customers["customer_id"].values


# Random customer for each order
order_customer = np.random.choice(
    customer_ids,
    N_ORDERS
)


# Brand distribution
brand_probs = [
    0.22,
    0.24,
    0.19,
    0.18,
    0.17
]


order_brands = np.random.choice(
    brand_names,
    N_ORDERS,
    p=brand_probs
)


# Random order dates
order_dates = pd.to_datetime(
    np.random.choice(
        dates,
        N_ORDERS
    )
)


# IMPORTANT:
# These probabilities add up to exactly 1.00
status_probabilities = [
    0.82,   # Delivered
    0.08,   # Cancelled
    0.10    # RTO
]


rows = []


for i in range(N_ORDERS):

    # Select brand
    brand = order_brands[i]

    info = brands[brand]


    # Select one product belonging to that brand
    brand_products = products[
        products["brand"] == brand
    ]


    product = brand_products.sample(
        1
    ).iloc[0]


    # Quantity purchased
    quantity = np.random.choice(
        [1, 1, 1, 2, 2, 3],
        p=[
            0.42,
            0.20,
            0.18,
            0.10,
            0.07,
            0.03
        ]
    )


    # Product price
    selling_price = float(
        product["selling_price"]
    )


    # Discount
    discount_percentage = np.random.choice(
        [0, 0.05, 0.10, 0.15],
        p=[
            0.45,
            0.30,
            0.20,
            0.05
        ]
    )


    discount = round(
        selling_price *
        quantity *
        discount_percentage,
        2
    )


    # Cost of goods sold
    cogs = round(
        float(product["cost_price"]) *
        quantity,
        2
    )


    # Shipping cost
    shipping = round(
        info["shipping"] *
        np.random.uniform(
            0.85,
            1.20
        ),
        2
    )


    # Marketing channel
    channel = np.random.choice(
        channels,
        p=[
            0.32,
            0.23,
            0.22,
            0.13,
            0.10
        ]
    )


    # Order status
    status = np.random.choice(
        statuses,
        p=status_probabilities
    )


    # Revenue after discount
    gross_revenue = (
        selling_price *
        quantity
    )


    revenue = round(
        gross_revenue -
        discount,
        2
    )


    rows.append({

        "order_id":
            f"O{i + 1:06d}",

        "order_date":
            order_dates[i],

        "brand":
            brand,

        "customer_id":
            order_customer[i],

        "product_id":
            product["product_id"],

        "quantity":
            quantity,

        "selling_price":
            round(
                selling_price,
                2
            ),

        "discount":
            discount,

        "cogs":
            cogs,

        "shipping_cost":
            shipping,

        "marketing_channel":
            channel,

        "status":
            status,

        "revenue":
            revenue
    })


orders = pd.DataFrame(rows)


orders.to_csv(
    DATA / "orders.csv",
    index=False
)


# ============================================================
# 9. MARKETING DATASET
# ============================================================

marketing_rows = []


for date in dates:

    for brand in brand_names:

        for channel in channels:

            base_spend = {

                "Meta Ads": 450,

                "Google Ads": 350,

                "Organic": 40,

                "Influencer": 220,

                "Email": 80

            }[channel]


            # Different marketing intensity
            # for different brands

            multiplier = {

                "AuraGlow": 1.10,

                "UrbanThread": 1.25,

                "HomeNest": 1.05,

                "TechEase": 1.20,

                "WellRoot": 0.85

            }[brand]


            # Daily advertising spend
            spend = max(
                10,
                np.random.normal(
                    base_spend * multiplier,
                    base_spend * 0.18
                )
            )


            # Impressions
            impressions = int(
                spend *
                np.random.uniform(
                    35,
                    65
                )
            )


            # Clicks
            clicks = int(
                impressions *
                np.random.uniform(
                    0.015,
                    0.045
                )
            )


            marketing_rows.append({

                "date":
                    date,

                "brand":
                    brand,

                "channel":
                    channel,

                "impressions":
                    impressions,

                "clicks":
                    clicks,

                "ad_spend":
                    round(
                        spend,
                        2
                    )
            })


marketing = pd.DataFrame(
    marketing_rows
)


marketing.to_csv(
    DATA / "marketing.csv",
    index=False
)


# ============================================================
# 10. WEBSITE FUNNEL DATASET
# ============================================================

funnel_rows = []


# Conversion behavior by brand

funnel_rates = {

    "AuraGlow":
        [0.42, 0.13, 0.48, 0.72],

    "UrbanThread":
        [0.34, 0.09, 0.36, 0.62],

    "HomeNest":
        [0.38, 0.11, 0.44, 0.66],

    "TechEase":
        [0.40, 0.10, 0.42, 0.60],

    "WellRoot":
        [0.46, 0.14, 0.52, 0.75]
}


# Average daily website sessions

traffic = {

    "AuraGlow": 1250,

    "UrbanThread": 1550,

    "HomeNest": 1000,

    "TechEase": 1150,

    "WellRoot": 900
}


for date in dates:

    for brand in brand_names:

        # Generate website traffic
        sessions = int(
            np.random.normal(
                traffic[brand],
                180
            )
        )


        # Prevent negative/very low traffic
        sessions = max(
            200,
            sessions
        )


        # Brand-specific funnel rates
        (
            view_rate,
            atc_rate,
            checkout_rate,
            purchase_rate
        ) = funnel_rates[brand]


        # Website funnel

        product_views = int(
            sessions *
            np.random.normal(
                view_rate,
                0.025
            )
        )


        add_to_cart = int(
            product_views *
            np.random.normal(
                atc_rate,
                0.012
            )
        )


        checkout = int(
            add_to_cart *
            np.random.normal(
                checkout_rate,
                0.025
            )
        )


        purchases = int(
            checkout *
            np.random.normal(
                purchase_rate,
                0.025
            )
        )


        funnel_rows.append({

            "date":
                date,

            "brand":
                brand,

            "sessions":
                sessions,

            "product_views":
                max(
                    0,
                    product_views
                ),

            "add_to_cart":
                max(
                    0,
                    add_to_cart
                ),

            "checkout":
                max(
                    0,
                    checkout
                ),

            "purchases":
                max(
                    0,
                    purchases
                )
        })


funnel = pd.DataFrame(
    funnel_rows
)


funnel.to_csv(
    DATA / "website_funnel.csv",
    index=False
)


# ============================================================
# 11. FINAL OUTPUT
# ============================================================

print()
print("=" * 50)
print("DATASET GENERATED SUCCESSFULLY")
print("=" * 50)

print(
    f"Orders: {len(orders):,}"
)

print(
    f"Customers: {len(customers):,}"
)

print(
    f"Products: {len(products):,}"
)

print(
    f"Marketing rows: {len(marketing):,}"
)

print(
    f"Funnel rows: {len(funnel):,}"
)

print()
print("Files created:")
print("1. data/products.csv")
print("2. data/customers.csv")
print("3. data/orders.csv")
print("4. data/marketing.csv")
print("5. data/website_funnel.csv")

print("=" * 50)