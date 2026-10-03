-- New vs repeat customer analysis
WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM orders
    WHERE status = 'Delivered'
    GROUP BY customer_id
)
SELECT
    CASE
        WHEN order_count = 1 THEN 'New / One-time'
        ELSE 'Repeat'
    END AS customer_type,
    COUNT(*) AS customers
FROM customer_orders
GROUP BY customer_type;
