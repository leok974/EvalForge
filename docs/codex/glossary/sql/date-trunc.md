---
id: glossary/sql/date-trunc
title: date_trunc
world: sql
---

# date_trunc

The `date_trunc` function is the primary tool in PostgreSQL for "bucketing" or "rounding" timestamps. It truncates a timestamp to a specified precision (like day, hour, or month).

## Why use it?
When analyzing high-velocity data (like logs or sensor readings), timestamps are often unique down to the millisecond. If you want to see "events per day," you need to group all timestamps from that day into a single "bucket."

## Syntax
```sql
date_trunc('precision', timestamp)
```

## Common Precisions
- `'year'`: 2023-04-15 10:30:00 -> 2023-01-01 00:00:00
- `'month'`: 2023-04-15 10:30:00 -> 2023-04-01 00:00:00
- `'day'`: 2023-04-15 10:30:00 -> 2023-04-15 00:00:00
- `'hour'`: 2023-04-15 10:30:00 -> 2023-04-15 10:00:00

## Example
```sql
SELECT 
    date_trunc('day', created_at) AS day,
    count(*) AS signups
FROM users
GROUP BY 1
ORDER BY 1 DESC;
```

> [!NOTE]
> Unlike `strftime` in SQLite, `date_trunc` returns a real **TIMESTAMPTZ** or **TIMESTAMP** object, not a string. This makes it much easier to perform further date math on the result.
