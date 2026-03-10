# Hints: Date Bucketing & Grouping

## Hint 1 — Transforming Dates
To strip the time off your timestamps, use the `strftime` function with the correct format string.
`strftime('%Y-%m-%d', event_date) AS event_date_only`

## Hint 2 — Counting Groups
To count events per day, you need to group by the transformed date.
`GROUP BY event_date_only`

## Hint 3 — The Full Query
```sql
SELECT 
    strftime('%Y-%m-%d', event_date) AS event_date_only, 
    COUNT(*) AS num_events 
FROM events 
GROUP BY event_date_only 
ORDER BY event_date_only ASC;
```
