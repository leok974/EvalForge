# cte-with

A **CTE** (Common Table Expression) is a temporary result set that you can reference within a `SELECT`, `INSERT`, `UPDATE`, or `DELETE` statement. It is defined using the `WITH` keyword.

## Syntax

```sql
WITH expression_name AS (
    SELECT ... (CTE Query)
)
SELECT ... FROM expression_name;
```

## Benefits

- **Readability**: Breaks complex queries into logical, named steps.
- **Reusability**: You can reference the same CTE multiple times in the main query.
- **Isolation**: Helps separate data preparation from final analysis.

## Example

```sql
WITH SalesByRegion AS (
    SELECT region, SUM(amount) as total
    FROM orders
    GROUP BY region
)
SELECT * FROM SalesByRegion WHERE total > 10000;
```
