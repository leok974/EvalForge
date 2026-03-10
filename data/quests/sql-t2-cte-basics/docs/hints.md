# Hints: CTE Basics (WITH)

## Hint 1 — Defining the CTE
Start your query with the `WITH` keyword followed by the name of your temporary view.
`WITH EventCounts AS ( ... your query ... )`

## Hint 2 — Filtering the View
Once the CTE is defined, you treat it like a regular table in your main `SELECT`.
`SELECT * FROM EventCounts WHERE num_events > 1;`

## Hint 3 — The Full Structure
```sql
WITH EventCounts AS (
    SELECT event_type, COUNT(*) as num_events 
    FROM events 
    GROUP BY event_type
) 
SELECT event_type, num_events 
FROM EventCounts 
WHERE num_events > 1 
ORDER BY event_type ASC;
```
