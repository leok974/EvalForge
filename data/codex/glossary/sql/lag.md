# lag

The `LAG()` function is a [window function](glossary/sql/window-function) that allows you to access data from a previous row in the same result set without the need for a self-join.

## Syntax

```sql
LAG(expression, offset, default) OVER (
    [PARTITION BY partition_expression]
    ORDER BY sort_expression
)
```

- **expression**: The column or calculation you want to retrieve.
- **offset**: (Optional) How many rows to look back. Defaults to 1.
- **default**: (Optional) The value to return if the offset goes before the first row. Defaults to `NULL`.

## Usage

`LAG()` is commonly used to calculate **Month-over-Month (MoM) growth** or differences between consecutive time periods.

```sql
SELECT 
    month, 
    revenue,
    LAG(revenue) OVER (ORDER BY month) as previous_month_revenue
FROM sales;
```

In this example, for each month, the query retrieves the revenue from the row immediately preceding it (the previous month).
