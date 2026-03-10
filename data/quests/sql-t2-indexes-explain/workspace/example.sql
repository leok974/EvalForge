-- Example: Explaining a primary key lookup
-- Primary keys are indexed automatically, so this should show a SEARCH
EXPLAIN QUERY PLAN 
SELECT * FROM employees WHERE id = 1;
