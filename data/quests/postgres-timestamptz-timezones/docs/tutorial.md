## Concept
When building global applications, time management is critical. PostgreSQL provides the `TIMESTAMPTZ` (Timestamp with Time Zone) data type to safely store an absolute point in time.

Internally, Postgres stores this as UTC. When you read it back, it is formatted to the session's time zone or remains UTC.

## Why It Matters
If you use a simple `TIMESTAMP` (without time zone) to record an event, the database doesn't know if that 9:00 AM happened in Tokyo, London, or New York. This leads to massive bugs when querying events across regions. 

`TIMESTAMPTZ` solves this by forcing the data to represent an absolute moment in time globally.

## Syntax Pattern
To convert a `TIMESTAMPTZ` column into a specific local time for reporting, use `AT TIME ZONE`:
```sql
SELECT column_name AT TIME ZONE 'Continent/City' AS local_time
FROM table_name;
```

## Example
If an employee was hired at `09:00:00 UTC`, and we want to know what time that was in Los Angeles:
```sql
SELECT hired_at AT TIME ZONE 'America/Los_Angeles' AS pt_hired_at
FROM employees;
```
*Note: This will return a `TIMESTAMP` without time zone, representing the local wall-clock time in LA.*

## Common Mistake
Storing user events as `TIMESTAMP` (without time zone) instead of `TIMESTAMPTZ`. If your server moves, or you have users in multiple countries, all your stored events lose their context and timezone conversions become impossible.
