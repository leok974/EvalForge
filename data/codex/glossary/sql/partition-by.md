# PARTITION BY

## Definition
`PARTITION BY` splits rows into groups for window functions. The window function runs separately within each partition.

## Tiny example
Rank orders per customer:
```sql
ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC)
```

## Common pitfall
Forgetting to partition causes calculations across the entire dataset (global rank), which is often wrong for per-user or per-group analytics.

## Related
OVER, Window Function
