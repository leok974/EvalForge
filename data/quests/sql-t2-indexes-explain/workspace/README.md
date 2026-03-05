# Mission: Indexes & EXPLAIN
**Goal**:
1. Open `task.sql`.
2. Add a `CREATE INDEX idx_emp_mgr ON employees(manager_id);` statement.
3. Add an `EXPLAIN QUERY PLAN SELECT * FROM employees WHERE manager_id = 1;` statement at the very end.
The test runner executes the final SQL statement and returns the `id, parent, notused, detail` output in SQLite.