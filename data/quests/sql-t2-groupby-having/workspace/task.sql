-- sql-t2-groupby-having
-- TASK: 
-- Identify high-volume product categories.
-- Return each category and the count of products in it.
--
-- Output columns (exact order):
--   category, count
--
-- Rules:
-- - Only include categories with MORE THAN 5 products
-- - Use the HAVING clause for the filter
--
-- TODO:
-- Add the missing group-level filter to the query below.

SELECT 
    category, 
    COUNT(*) as count
FROM products
GROUP BY category;
