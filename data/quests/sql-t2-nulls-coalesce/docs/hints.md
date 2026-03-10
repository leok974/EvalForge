# Hints: NULL Semantics & COALESCE

## Hint 1 — Basic Addition
To find total compensation, you need to add the `salary` and `bonus` columns.
`salary + bonus AS total_comp`

## Hint 2 — The NULL Problem
If an employee has no bonus (`NULL`), adding it to their salary will result in `NULL`. Use the `COALESCE` function to provide a fallback of 0.
`COALESCE(bonus, 0)`

## Hint 3 — Sorting
Remember to sort the results first by your new calculated column, then by ID to break ties.
`ORDER BY total_comp DESC, id ASC;`

## Hint 4 — The Full Query
Combine these pieces into your final SELECT statement.
```sql
SELECT id, name, salary + COALESCE(bonus, 0) AS total_comp
FROM employees
ORDER BY total_comp DESC, id ASC;
```
