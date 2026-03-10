# correlated-subquery

A **correlated subquery** is a [subquery](glossary/sql/subquery) that uses values from the outer query. This makes the subquery dependent on the outer query, causing it to be executed once for every row processed by the outer query.

## Comparison

- **Normal Subquery**: Can be executed once, independently of the outer query.
- **Correlated Subquery**: References outer columns (e.g., `o.id`), requiring it to run repeatedly.

## Example

```sql
-- Find employees who earn more than the average in THEIR department
SELECT name, salary, department
FROM employees e1
WHERE salary > (
    SELECT AVG(salary)
    FROM employees e2
    WHERE e2.department = e1.department
);
```

In this query, `e1.department` links the inner query to the current row of the outer query.
