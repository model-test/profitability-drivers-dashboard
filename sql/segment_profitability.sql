WITH segment_totals AS (
    SELECT c.segment,
           ROUND(SUM(o.revenue), 2) AS segment_revenue,
           ROUND(SUM(o.profit), 2) AS segment_profit,
           SUM(SUM(o.revenue)) OVER() AS total_revenue,
           SUM(SUM(o.profit)) OVER() AS total_profit
    FROM customers AS c
    INNER JOIN orders AS o
        ON o.customer_id = c.customer_id
    GROUP BY c.segment
),
segment_analysis AS (
    SELECT segment,
           segment_revenue,
           ROUND(segment_revenue / NULLIF(total_revenue, 0) * 100, 2) AS revenue_contribution_pct,
           segment_profit,
           ROUND(segment_profit / NULLIF(total_profit, 0) * 100, 2) AS profit_contribution_pct,
           ROUND(segment_profit * 1.0 / NULLIF(segment_revenue, 0) * 100, 2) AS profit_margin_pct,
           ROUND(total_profit * 1.0 / NULLIF(total_revenue, 0) * 100, 2) AS overall_profit_margin_pct
    FROM segment_totals
)
SELECT segment,
       segment_revenue,
       revenue_contribution_pct,
       segment_profit,
       profit_contribution_pct,
       profit_margin_pct,
       overall_profit_margin_pct,
       ROUND(profit_margin_pct - overall_profit_margin_pct, 2) AS profit_margin_difference
FROM segment_analysis
ORDER BY segment_revenue DESC;
