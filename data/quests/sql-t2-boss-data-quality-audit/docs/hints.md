# Hints: BOSS - Data Quality Audit

## Hint 1 — Creating the Problem
Start by inserting the "Ghost Employee" provided in the instructions. This record has a manager ID (999) that doesn't correspond to any actual employee.

## Hint 2 — The Anti-Join
To find orphans, join the table to itself on `manager_id = id`. 
`LEFT JOIN employees m ON e.manager_id = m.id`

## Hint 3 — Filtering for Voids
Filter the joined result for rows where the *manager's* ID is NULL, but the *employee's* manager_id was NOT NULL.
`WHERE e.manager_id IS NOT NULL AND m.id IS NULL`

## Hint 4 — The Full Solution
```sql
INSERT INTO employees (id, name, manager_id) VALUES (99, 'Ghost Employee', 999);

SELECT e.id, e.name, e.manager_id 
FROM employees e 
LEFT JOIN employees m ON e.manager_id = m.id 
WHERE e.manager_id IS NOT NULL AND m.id IS NULL 
ORDER BY e.id ASC;
```
