-- Contribution profitability by brand
SELECT
    brand,
    SUM(revenue) AS revenue,
    SUM(cogs) AS cogs,
    SUM(shipping_cost) AS shipping_cost,
    SUM(revenue - cogs - shipping_cost) AS contribution_profit,
    100.0 * SUM(revenue - cogs - shipping_cost)
        / NULLIF(SUM(revenue), 0) AS contribution_margin_pct
FROM orders
WHERE status = 'Delivered'
GROUP BY brand
ORDER BY contribution_margin_pct DESC;
