-- Funnel conversion by brand
SELECT
    brand,
    SUM(sessions) AS sessions,
    SUM(product_views) AS product_views,
    SUM(add_to_cart) AS add_to_cart,
    SUM(checkout) AS checkout,
    SUM(purchases) AS purchases,
    100.0 * SUM(purchases) / NULLIF(SUM(sessions), 0) AS session_to_purchase_rate,
    100.0 * SUM(add_to_cart) / NULLIF(SUM(product_views), 0) AS view_to_cart_rate,
    100.0 * SUM(checkout) / NULLIF(SUM(add_to_cart), 0) AS cart_to_checkout_rate
FROM website_funnel
GROUP BY brand;
