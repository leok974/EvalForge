# Window Function

## Definition
A **window function** computes a value across a related set of rows while keeping each row in the output. Unlike `GROUP BY`, it does not collapse rows.

## Tiny example
```sql
SELECT
  customer_id,
  amount,
  ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY amount DESC) AS rn
FROM orders;
```

## Common pitfall
Using `GROUP BY` when you want row-level results. If you need “one row per original row plus extra computed columns,” window functions are usually the right tool.

## Related
OVER, PARTITION BY
