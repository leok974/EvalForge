# cte-recursive

A **recursive CTE** is a [CTE](glossary/sql/cte-with) that references itself. It is used to query hierarchical data, such as organizational charts, file systems, or family trees.

## Structure

A recursive CTE has three main parts:
1. **Anchor Member**: The initial query that returns the base result set (e.g., the CEO in an org chart).
2. **Recursive Member**: A query that joins the base table with the CTE itself.
3. **UNION ALL**: The operator that combines the results of the anchor and recursive members.

## Example

```sql
WITH RECURSIVE OrgChart AS (
    -- Anchor: Level 0 (The CEO)
    SELECT id, name, manager_id, 0 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursion: Move down the management chain
    SELECT e.id, e.name, e.manager_id, o.level + 1
    FROM employees e
    JOIN OrgChart o ON e.manager_id = o.id
)
SELECT * FROM OrgChart;
```

SQL will continue running the recursive member until no more rows are returned.
