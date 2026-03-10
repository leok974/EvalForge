# Hints: Window Functions (RANK)

## Hint 1 — The Clause
To perform a calculation across a set of rows without collapsing them, use the `OVER` clause.
`RANK() OVER(...)`

## Hint 2 — Partitioning
To reset the rank for each department, use `PARTITION BY`.
`PARTITION BY department`

## Hint 3 — Ordering
To ensure the highest salary is rank #1, use `ORDER BY` inside the window.
`ORDER BY salary DESC`

## Hint 4 — The Full Query
```sql
SELECT 
    name, 
    department, 
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employees;
```
