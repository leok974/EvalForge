# Tutorial: NULL Semantics & COALESCE

In SQL, [NULL](glossary/sql/null) represents a missing or unknown value. While it sounds simple, `NULL` behaves differently than zero or an empty string, especially during calculations.

## The Problem with NULL in Math

Any arithmetic operation involving `NULL` results in `NULL`.

- `100 + 50 = 150`
- `100 + NULL = NULL`

If an employee's total compensation is `salary + bonus`, and their `bonus` is `NULL`, their total compensation will unfortunately become `NULL` as well.

## Enter COALESCE

The `COALESCE()` function allows you to provide a **fallback value** for `NULL`. It takes a list of arguments and returns the first one that is NOT `NULL`.

```sql
SELECT 
  name,
  salary + COALESCE(bonus, 0) AS total_comp
FROM employees;
```

In this example:
1. If `bonus` is `5000`, `COALESCE(bonus, 0)` returns `5000`.
2. If `bonus` is `NULL`, `COALESCE(bonus, 0)` returns `0`.

This ensures the addition always works, even if the bonus is missing.

## Proper NULL Comparison

Remember: you cannot use `=` to check for `NULL`.
- ❌ `WHERE bonus = NULL` (Always UNKNOWN)
- ✅ `WHERE bonus IS NULL`

In this quest, you will use `COALESCE` to calculate accurate total compensation for a list of employees.
