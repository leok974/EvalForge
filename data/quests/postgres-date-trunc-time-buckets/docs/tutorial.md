# Time Bucketing with DATE_TRUNC

`DATE_TRUNC` truncates a timestamp to a specified precision, effectively grouping timestamps into buckets.

## Syntax

```sql
DATE_TRUNC('unit', timestamp_column)
```

Common units: `'second'`, `'minute'`, `'hour'`, `'day'`, `'month'`, `'year'`

## Example: hourly counts

```sql
SELECT
    DATE_TRUNC('hour', created_at) AS hour_bucket,
    COUNT(*)                        AS event_count
FROM events
WHERE created_at >= '2024-03-01'
  AND created_at <  '2024-03-02'
GROUP BY hour_bucket
ORDER BY hour_bucket;
```

This query returns one row per hour that had at least one event.

## Why use a half-open interval?

```sql
WHERE recorded_at >= '2024-01-15'
  AND recorded_at <  '2024-01-16'
```

Using `< '2024-01-16'` (exclusive upper bound) is safer than `<= '2024-01-15 23:59:59'` because it handles all sub-second timestamps correctly.

## Alias in GROUP BY

After defining `DATE_TRUNC(...) AS hour_bucket` in the SELECT, you can reference the alias in GROUP BY:

```sql
GROUP BY hour_bucket
```

This is allowed in PostgreSQL and makes the query more readable.
