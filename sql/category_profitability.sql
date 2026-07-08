WITH category_totals AS (
    SELECT p.category,
           ROUND(SUM(o.revenue), 2) AS category_revenue,
           ROUND(SUM(o.profit), 2) AS category_profit,
           SUM(SUM(o.revenue)) OVER() AS total_revenue,
           SUM(SUM(o.profit)) OVER() AS total_profit
    FROM products AS p
    INNER JOIN orders AS o
        ON o.product_id = p.product_id
    GROUP BY p.category
),
category_analysis AS (
    SELECT category,
           category_revenue,
           ROUND(category_revenue / NULLIF(total_revenue, 0) * 100, 2) AS revenue_contribution_pct,
           category_profit,
           ROUND(category_profit / NULLIF(total_profit, 0) * 100, 2) AS profit_contribution_pct,
           ROUND(category_profit * 1.0 / NULLIF(category_revenue, 0) * 100, 2) AS profit_margin_pct,
           ROUND(total_profit * 1.0 / NULLIF(total_revenue, 0) * 100, 2) AS overall_profit_margin_pct
    FROM category_totals
)
SELECT category,
       category_revenue,
       revenue_contribution_pct,
       category_profit,
       profit_contribution_pct,
       profit_margin_pct,
       overall_profit_margin_pct,
       ROUND(profit_margin_pct - overall_profit_margin_pct, 2) AS profit_margin_difference
FROM category_analysis
ORDER BY category_revenue DESC;
