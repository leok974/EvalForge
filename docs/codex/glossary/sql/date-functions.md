---
id: glossary/sql/date-functions
title: date-functions
world: sql
---

# date-functions

**Date functions** allow you to manipulate, format, and calculate values based on time and date data.

## Common Functions (SQLite)

- `date()`: Returns a date string (YYYY-MM-DD).
- `time()`: Returns a time string (HH:MM:SS).
- `datetime()`: Returns both.
- `strftime(format, date)`: Formats a date string according to a specific pattern.

## Example: strftime

```sql
-- Extract only the year-month from a timestamp
SELECT strftime('%Y-%m', event_date) as month
FROM events;
```

Date functions are critical for "bucketing" data into daily, weekly, or monthly reports.