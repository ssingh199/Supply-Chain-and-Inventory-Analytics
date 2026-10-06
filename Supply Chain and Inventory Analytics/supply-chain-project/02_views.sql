USE supply_chain;

-- 1. Monthly sales trend with month-over-month growth
CREATE OR REPLACE VIEW vw_monthly_sales AS
WITH m AS (
  SELECT CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS month_start,
         COUNT(DISTINCT order_id)      AS orders,
         SUM(sales)                    AS sales,
         SUM(order_profit_per_order)   AS profit
  FROM fact_orders
  GROUP BY CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE)
)
SELECT month_start, orders, ROUND(sales, 2) AS sales, ROUND(profit, 2) AS profit,
       ROUND(100 * (sales - LAG(sales) OVER (ORDER BY month_start))
             / LAG(sales) OVER (ORDER BY month_start), 2) AS mom_growth_pct
FROM m;

-- 2. Delivery performance by market, region, shipping mode and year
CREATE OR REPLACE VIEW vw_delivery_performance AS
SELECT market, order_region, shipping_mode, YEAR(order_date) AS order_year,
       COUNT(*)                          AS order_items,
       SUM(is_late)                      AS late_items,
       ROUND(100 * AVG(is_late), 2)      AS late_pct,
       ROUND(AVG(shipping_delay_days), 2) AS avg_delay_days,
       ROUND(AVG(days_for_shipping_real), 2) AS avg_real_days
FROM fact_orders
GROUP BY market, order_region, shipping_mode, YEAR(order_date);

-- 3. Product ABC classification (A = first 80% of revenue, B = next 15%, C = last 5%)
CREATE OR REPLACE VIEW vw_product_abc AS
WITH ps AS (
  SELECT p.product_card_id, p.product_name, p.category_name,
         SUM(f.sales)                  AS revenue,
         SUM(f.order_item_quantity)    AS units_sold,
         SUM(f.order_profit_per_order) AS profit
  FROM fact_orders f
  JOIN dim_product p ON p.product_card_id = f.product_card_id
  GROUP BY p.product_card_id, p.product_name, p.category_name
),
ranked AS (
  SELECT ps.*,
         SUM(revenue) OVER (ORDER BY revenue DESC ROWS UNBOUNDED PRECEDING)
           / SUM(revenue) OVER () AS cum_share
  FROM ps
)
SELECT product_card_id, product_name, category_name,
       ROUND(revenue, 2) AS revenue, units_sold, ROUND(profit, 2) AS profit,
       ROUND(100 * cum_share, 2) AS cum_revenue_pct,
       CASE WHEN cum_share <= 0.80 THEN 'A'
            WHEN cum_share <= 0.95 THEN 'B'
            ELSE 'C' END AS abc_class
FROM ranked;