# Hints: Recursive CTEs (Hierarchy)

## Hint 1 — Joining the Tree
The recursive part of the CTE must join the base table (`employees`) to the CTE itself (`OrgChart`) so that it can walk down the levels.
`JOIN OrgChart o ON e.manager_id = o.id`

## Hint 2 — Termination
SQL stops the recursion automatically when no more direct reports are found. You just need to select the final results from your temporary view.
`SELECT id, name, distance FROM OrgChart`

## Hint 3 — The Full Query
```sql
WITH RECURSIVE OrgChart AS (
    SELECT id, name, manager_id, 0 as distance
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, o.distance + 1
    FROM employees e
    JOIN OrgChart o ON e.manager_id = o.id
)
SELECT id, name, distance 
FROM OrgChart 
ORDER BY distance ASC, id ASC;
```
