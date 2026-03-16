---
id: world-sql/date-trunc
title: date-trunc
world: sql
---

# PostgreSQL: Date Truncation

The `date_trunc` function is essential for grouping time-series data into discrete buckets (e.g., by hour, day, week).

### Syntax
```sql
date_trunc('unit', timestamp)
```

Common units:
- `'hour'`: Groups all minutes/seconds into the start of that hour.
- `'day'`: Groups all activities on a specific calendar day.
- `'week'`: Align data to the start of the week (Monday).

### Example: Hourly Averages
```sql
SELECT 
    date_trunc('hour', recorded_at) AS hour_bucket,
    avg(temperature) as avg_temp
FROM sensor_readings
GROUP BY 1
ORDER BY 1;
```
