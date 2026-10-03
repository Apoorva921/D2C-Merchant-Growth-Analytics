-- Revenue by brand
SELECT
    brand,
    SUM(revenue) AS total_revenue,
    COUNT(DISTINCT order_id) AS orders,
    SUM(revenue) / NULLIF(COUNT(DISTINCT order_id), 0) AS aov
FROM orders
WHERE status = 'Delivered'
GROUP BY brand
ORDER BY total_revenue DESC;
