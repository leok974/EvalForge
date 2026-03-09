-- sql-cte-subquery
-- TASK:
-- The Archivist wants a clean report on the total spend of our active users.
--
-- Output columns:
--   user_name, total_spend
--
-- Requirements:
-- 1) Use a [CTE](glossary/sql/cte) to filter for active users first. name the CTE 'active_users'.
-- 2) Join this CTE with the orders table.
-- 3) Calculate the SUM(total_cents) as total_spend for each user from the CTE.
-- 4) Return the user_name and total_spend.
--
-- Rules:
-- - Use the WITH clause for the CTE.
-- - Group by the user name.
--
-- TODO:
-- Write a query that uses a CTE to calculate spend for active users.

SELECT
  name
FROM users
WHERE is_active = 1;
