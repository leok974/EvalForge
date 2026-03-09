-- sql-joins
-- TASK:
-- The Logistics team needs to know which user placed each order.
--
-- Output columns (exact order):
--   order_id, user_name
--
-- Requirements:
-- 1) [JOIN](glossary/sql/join) the orders table with the users table.
-- 2) Connect them using the user_id from orders and the id from users.
-- 3) Return the order id (as order_id) and the user name (as user_name).
--
-- Rules:
-- - Use an INNER JOIN.
-- - Use the ON clause to specify the relationship.
--
-- TODO:
-- Write a query that joins orders and users.

SELECT
  id
FROM orders;
