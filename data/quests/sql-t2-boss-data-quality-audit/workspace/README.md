# Mission: BOSS Data Quality Audit
**Goal**:
Find all `manager_id`s in `employees` that do NOT have a corresponding valid `id` in the `employees` table (Orphaned Managers).
Return `id, name, manager_id` of the employees with the invalid manager_id.

*Wait, our DB is small and clean. Let's insert a dirty row first inside your query!* 
**Task**:
1. `INSERT INTO employees (id, name, manager_id) VALUES (99, 'Ghost Employee', 999);`
2. Write a single query (using a CTE or Anti-Join `NOT EXISTS` / `LEFT JOIN ... IS NULL`) to find the employee(s) who reference a missing manager.
3. Return `id, name, manager_id`. 
**Order**: By `id` ASC.