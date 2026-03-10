-- sql-t2-nulls-coalesce
-- TASK:
-- Calculate the total compensation for each employee.
--
-- Output columns (exact order):
--   id, name, total_comp
--
-- Rules:
-- - total_comp is salary + bonus
-- - If bonus is NULL, it should count as 0
-- - Sort by total_comp DESC, then id ASC
--
-- TODO:
-- Update the query below to include the total_comp calculation with COALESCE.

SELECT
  id,
  name
FROM employees;
