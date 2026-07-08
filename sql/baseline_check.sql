SELECT
    COUNT(*) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) * 1.0 / NULLIF(SUM(revenue), 0) * 100, 2) AS overall_profit_margin_pct
FROM orders;
