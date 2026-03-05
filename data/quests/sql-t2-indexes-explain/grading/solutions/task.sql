CREATE INDEX idx_emp_mgr ON employees(manager_id);
EXPLAIN QUERY PLAN SELECT * FROM employees WHERE manager_id = 1;