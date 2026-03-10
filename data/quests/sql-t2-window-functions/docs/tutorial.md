# Tutorial: Window Functions (RANK and OVER)

Standard [aggregation](glossary/sql/sum) (like `GROUP BY`) collapses multiple [rows](glossary/sql/row) into a single result. **Window Functions**, however, perform calculations across a set of rows while still keeping the individual rows visible.

## The OVER Clause

The `OVER` clause defines the "window" of rows that the function will look at.

```sql
SELECT 
  name, 
  salary,
  RANK() OVER (ORDER BY salary DESC) as global_rank
FROM employees;
```

## Partitioning

The `PARTITION BY` sub-clause is like a `GROUP BY` that doesn't collapse rows. It resets the window calculation for each category.

```sql
SELECT 
  name, 
  department,
  salary,
  RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
FROM employees;
```

In this example:
1. The rows are "partitioned" by `department`.
2. Within each department, rows are ordered by `salary`.
3. The `RANK()` function assigns a number (1, 2, 3...) based on that order.
4. When the department changes, the rank resets to 1.

In this quest, you will use `RANK()` and `PARTITION BY` to find the relative standing of employees within their own departments.
