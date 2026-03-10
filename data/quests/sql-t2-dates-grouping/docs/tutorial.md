# Tutorial: Date Bucketing & Grouping

In many databases, timestamps are high-precision (including hours, minutes, and seconds). When you want to count events by **day**, you need to "bucket" these timestamps into larger date blocks.

## The strftime Function

SQLite uses the `strftime(format, date_string)` function to format [dates](glossary/sql/date-functions).

Common format strings:
- `%Y`: Year (2023)
- `%m`: Month (01-12)
- `%d`: Day (01-31)
- `%H`: Hour (00-23)

To get just the date (YYYY-MM-DD), you use:
`strftime('%Y-%m-%d', event_date)`

## Bucketing in a Query

Once you have formatted the date, you can [group by](glossary/sql/group-by) that formatted value to see aggregate statistics per day.

```sql
SELECT 
  strftime('%Y-%m', event_date) AS month,
  COUNT(*) AS total_events
FROM events
GROUP BY month;
```

In this quest, you will use `strftime` to bucket events by day and count how much activity occurred each day in October.
