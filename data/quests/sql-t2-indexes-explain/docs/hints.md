# Hints: Indexes & EXPLAIN

## Hint 1 — Creating the Shortcut
To speed up lookups on a column, you need to create an index. Ensure your index name matches the requirements exactly.
`CREATE INDEX idx_emp_mgr ON employees(manager_id);`

## Hint 2 — Verifying the Plan
Prefix your query with `EXPLAIN QUERY PLAN` to see if the database uses your new index.
`EXPLAIN QUERY PLAN SELECT * FROM employees WHERE manager_id = 1;`

## Hint 3 — The Solution
Combine both commands. The seeder ensures the table is reset before your query runs, so you can safely create the index.
```sql
CREATE INDEX idx_emp_mgr ON employees(manager_id);
EXPLAIN QUERY PLAN SELECT * FROM employees WHERE manager_id = 1;
```
