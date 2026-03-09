-- sql-left-join-null
-- TASK:
-- We need to identify users who have remained silent — those who have never placed an order.
--
-- Output columns:
--   user_name
--
-- Requirements:
-- 1) [LEFT JOIN](glossary/sql/join) the users table with the orders table.
-- 2) Connect them using the id from users and the user_id from orders.
-- 3) Filter the results to only include rows where the order id is [NULL](glossary/sql/null).
-- 4) Return the user's name (as user_name).
--
-- Rules:
-- - Use LEFT JOIN so you don't lose users without orders.
-- - Use WHERE ... IS NULL to find the gap.
--
-- TODO:
-- Write a query that finds users with zero orders.

SELECT
  name
FROM users;
