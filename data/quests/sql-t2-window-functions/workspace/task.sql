-- sql-t2-window-functions
-- TASK:
-- Rank employees by salary within each department.
--
-- Output columns (exact order):
--   name, department, salary, rank
--
-- Rules:
-- - Use RANK() OVER(...) for the calculation
-- - Partition the ranking by department
-- - Order the rank by salary descending
--
-- TODO:
-- Add the RANK() window function to the query below.

SELECT
  name,
  department,
  salary,
  -- TODO: Calculate rank here
FROM employees;
