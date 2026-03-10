-- sql-t2-analytics-pack
-- TASK:
-- Calculate month-over-month revenue growth.
--
-- Output columns (exact order):
--   month, revenue, prev_revenue, growth
--
-- Rules:
-- - Use a CTE named 'LaggedSales' to calculate prev_revenue using LAG()
-- - In the main query, calculate growth as (revenue - prev_revenue)
-- - Exclude the first month where prev_revenue is NULL
-- - Sort by month ascending
--
-- TODO:
-- Use a CTE and the LAG() window function to complete the growth report.

WITH LaggedSales AS (
  SELECT 
    month, 
    revenue,
    -- TODO: Add LAG() over month here
  FROM monthly_sales
)
SELECT 
  * 
FROM LaggedSales;
