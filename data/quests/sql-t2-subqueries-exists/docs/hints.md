# Hints: Correlated Subqueries & EXISTS

## Hint 1 — Concept
`EXISTS` checks if a subquery returns at least one row. In a **correlated** subquery, the inner query references the outer query (e.g., `e1.id`).

## Hint 2 — The Subquery
You need to search for any row in the `employees` table where the `manager_id` matches the `id` of the employee from the outer query.
`WHERE EXISTS (SELECT 1 FROM employees e2 WHERE e2.manager_id = e1.id)`

## Hint 3 — The Full Query
```sql
SELECT id, name 
FROM employees e1 
WHERE EXISTS (
    SELECT 1 
    FROM employees e2 
    WHERE e2.manager_id = e1.id
) 
ORDER BY id ASC;
```
