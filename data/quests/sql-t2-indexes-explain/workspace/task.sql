-- sql-t2-indexes-explain
-- TASK:
-- Create an index to speed up manager lookups and verify it.
--
-- Output columns (exact order):
--   Plan description (from EXPLAIN)
--
-- Rules:
-- - Create index named 'idx_emp_mgr' on employees(manager_id)
-- - Run EXPLAIN QUERY PLAN on: SELECT * FROM employees WHERE manager_id = 1
--
-- TODO:
-- Add the index creation statement before the explanation.

-- TODO: CREATE INDEX idx_emp_mgr ON ...

EXPLAIN QUERY PLAN 
SELECT * FROM employees WHERE manager_id = 1;
