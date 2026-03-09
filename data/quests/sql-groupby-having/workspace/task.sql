-- sql-groupby-having
-- TASK:
-- The Archivist wants to know which categories of products are the most premium.
--
-- Output columns (exact order):
--   category, average_price
--
-- Requirements:
-- 1) Group products by their category.
-- 2) Calculate the average price_cents as average_price.
-- 3) Only include categories where the average_price is greater than 5000.
--
-- Rules:
-- - Use GROUP BY to bucket the products.
-- - Use HAVING to filter based on the average price.
--
-- TODO:
-- Write a query that groups products and filters categories.

SELECT
  category,
  price_cents
FROM products;
