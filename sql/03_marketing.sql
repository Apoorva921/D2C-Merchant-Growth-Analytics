-- Marketing performance
SELECT
    brand,
    channel,
    SUM(ad_spend) AS spend,
    SUM(clicks) AS clicks,
    SUM(impressions) AS impressions,
    100.0 * SUM(clicks) / NULLIF(SUM(impressions), 0) AS ctr
FROM marketing
GROUP BY brand, channel
ORDER BY brand, spend DESC;
