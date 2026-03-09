-- sql-aggregates
-- TASK:
-- The Archivist needs a high-level summary of our product inventory.
--
-- Output columns (exact order):
--   total_count, total_value_cents
--
-- Rules:
-- - Use COUNT(*) for the total number of products.
-- - Use SUM(price_cents) for the total value.
-- - Use AS to name the columns correctly.
--
-- TODO:
-- Write a query that summarizes the products table.

SELECT
  name
FROM products;
