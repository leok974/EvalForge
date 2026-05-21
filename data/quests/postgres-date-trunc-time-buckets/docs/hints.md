## Hint 1
Use `DATE_TRUNC('hour', recorded_at) AS hour_bucket` in your SELECT clause to truncate each timestamp to the start of its hour.

## Hint 2
Add a WHERE clause with a half-open interval: `WHERE recorded_at >= '2024-01-15' AND recorded_at < '2024-01-16'` to filter to the target day.

## Hint 3
Add `GROUP BY hour_bucket` and `ORDER BY hour_bucket`. The expected result is 4 rows (4 distinct hours with readings on that day).
