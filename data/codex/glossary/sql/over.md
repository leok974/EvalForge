# OVER

## Definition
`OVER (...)` defines the window for a window function: how rows are grouped and ordered for computation.

## Tiny example
```sql
SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date)
```

## Common pitfall
Omitting `ORDER BY` inside `OVER` when you need a running total or rank. Without ordering, the calculation may not match the intended sequence.

## Related
Window Function, ORDER BY
