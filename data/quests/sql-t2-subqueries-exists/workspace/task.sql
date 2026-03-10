-- sql-t2-subqueries-exists
-- TASK:
-- Find all employees who have at least one direct report.
--
-- Output columns (exact order):
--   id, name
--
-- Rules:
-- - Use the EXISTS operator with a correlated subquery
-- - Sort by id ascending
--
-- TODO:
-- Update the query below to only include employees whose ID exists as a manager_id in the employees table.

SELECT
  id,
  name
FROM employees e1
-- TODO: Add WHERE EXISTS (...)
ORDER BY id ASC;
