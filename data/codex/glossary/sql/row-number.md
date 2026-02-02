# ROW_NUMBER

## Definition
`ROW_NUMBER()` assigns a unique sequential integer to rows within a window partition, based on the window’s ordering.

## Tiny example
```sql
ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC)
```

## Common pitfall
`ROW_NUMBER` breaks ties arbitrarily (still unique). If you want ties to share ranks, look at `RANK()` or `DENSE_RANK()` instead.

## Related
ORDER BY, PARTITION BY
