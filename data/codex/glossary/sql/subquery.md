# subquery

A **subquery** (also known as an inner query or nested query) is a query within another SQL query, embedded in the `WHERE`, `FROM`, or `SELECT` clause.

## Common Types

- **Scalar Subquery**: Returns a single value.
- **Table Subquery**: Returns a set of rows and columns (often used in the `FROM` clause).
- **Correlated Subquery**: A subquery that references columns from the outer query.

## Example

```sql
-- Find employees with a salary higher than the average
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

In this example, the inner query `(SELECT AVG(salary) FROM employees)` runs first, and its result is used by the outer query's `WHERE` clause.
