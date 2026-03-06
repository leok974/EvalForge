# Tutorial: The WHERE Clause

The `WHERE` clause filters rows **before** they reach your result set. Without it, every row is returned.

## Basic syntax

```sql
SELECT column1, column2
FROM table_name
WHERE condition;
```

## Filtering with equality

```sql
SELECT name FROM users WHERE city = 'Detroit';
-- Returns: Alice, Charlie
```

## Filtering with a boolean flag

SQLite stores booleans as integers (`1` = true, `0` = false):

```sql
SELECT name FROM users WHERE is_active = 1;
```

## Combining with ORDER BY

Filters happen **before** sorting:

```sql
SELECT id, name, city
FROM users
WHERE is_active = 1
ORDER BY name ASC;
```

## For this quest

The `users` table has 6 rows. Two users (`Charlie`, `Evan`) have `is_active = 0`.
Your query should return the **4 active users**, sorted alphabetically:

| id | name  | city    |
|----|-------|---------|
| 1  | Alice | Detroit |
| 2  | Bob   | Austin  |
| 4  | Diana | Seattle |
| 6  | Fay   | Miami   |
