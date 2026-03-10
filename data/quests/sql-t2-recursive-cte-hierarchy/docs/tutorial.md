# Tutorial: Recursive CTEs (Hierarchy)

Most SQL queries work on "flat" data. But many real-world datasets are **hierarchical**, such as an organizational chart (employees and managers) or a folder structure. 

To traverse these relationships, you use a **Recursive CTE**.

## The Anatomy of a Recursive CTE

A recursive CTE consists of three parts combined by a `UNION ALL`:

1. **The Anchor Member**: The starting point of the recursion (e.g., the CEO, who has no manager).
2. **The Recursive Member**: A query that joins the table back to the CTE itself (e.g., "Find everyone who reports to the people found in the previous step").
3. **The Termination Condition**: Implicitly, the recursion stops when the recursive member returns no more rows.

```sql
WITH RECURSIVE OrgChart AS (
  -- Anchor: Find the top-level bosses
  SELECT id, name, manager_id, 0 as distance
  FROM employees
  WHERE manager_id IS NULL

  UNION ALL

  -- Recursion: Find their direct reports
  SELECT e.id, e.name, e.manager_id, o.distance + 1
  FROM employees e
  JOIN OrgChart o ON e.manager_id = o.id
)
SELECT * FROM OrgChart;
```

## Calculating "Distance"

By adding `o.distance + 1` in the recursive member, you can track how many "hops" away each person is from the anchor. In an org chart, this represents their "level" in the hierarchy.

In this quest, you will build a complete organizational chart starting from the CEO and calculating each employee's distance from the top.
