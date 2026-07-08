import pandas as pd
import sqlite3

conn = sqlite3.connect("mini_project.db")

customers_df = pd.read_csv("customers.csv")
products_df = pd.read_csv("products.csv")
orders_df = pd.read_csv("orders.csv")

customers_df.to_sql("customers", conn, if_exists="replace", index=False)
products_df.to_sql("products", conn, if_exists="replace", index=False)
orders_df.to_sql("orders", conn, if_exists="replace", index=False)

# BASELINE CHECK

query = """
SELECT
    COUNT(*) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) * 1.0 / NULLIF(SUM(revenue), 0) * 100, 2) AS overall_profit_margin_pct
FROM orders;
"""

baseline_check = pd.read_sql_query(query, conn)

print(baseline_check.to_string(index=False))

baseline_check.to_csv("baseline_data.csv", index=False)

# CATEGORY PROFITABILITY

query = """
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
"""

category_profitability = pd.read_sql_query(query, conn)

print(category_profitability.to_string(index=False))

category_profitability.to_csv("category_profitability.csv", index=False)

# SEGMENT PROFITABILITY

query = """
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
"""

segment_profitability = pd.read_sql_query(query, conn)

print(segment_profitability.to_string(index=False))

segment_profitability.to_csv("segment_profitability.csv", index=False)
