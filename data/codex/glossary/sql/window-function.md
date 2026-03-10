# window-function

A **window function** performs a calculation across a set of table rows that are somehow related to the current row. Unlike aggregate functions, window functions do not collapse rows into a single output; they retain the identity of each row.

## Key Concept: OVER()

The `OVER()` clause defines the "window" of rows that the function operates on.

## Syntax

```sql
FUNCTION_NAME() OVER (
    [PARTITION BY partition_col]
    [ORDER BY sort_col]
)
```

## Common Window Functions

- `RANK()`: Assigns a rank to each row within a partition.
- `ROW_NUMBER()`: Assigns a unique sequential integer to rows.
- `LAG()`: Accesses data from a previous row.
- `LEAD()`: Accesses data from a subsequent row.

## Usage

Window functions are essential for advanced analytics, such as running totals, moving averages, and ranking data within categories (e.g., "Top 3 employees per department").
