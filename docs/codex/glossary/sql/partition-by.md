---
id: glossary/sql/partition-by
title: partition-by
world: sql
---

# partition-by

The `PARTITION BY` clause is used within [window functions](glossary/sql/window-function) to divide the result set into partitions to which the function is applied separately.

## How it works

If you think of a window function as calculating a value over a "window" of rows, `PARTITION BY` allows you to reset that window whenever the value in a specific column changes.

## Example

```sql
SELECT 
    name, 
    department, 
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
FROM employees;
```

In this example:
1. The rows are divided into groups based on their `department`.
2. The `RANK()` function calculates the salary rank **within each department**.
3. When the query moves to a new department, the rank starts over at 1.