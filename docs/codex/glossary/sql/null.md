---
id: glossary/sql/null
level: beginner
related:
- codex:glossary/sql/where
- codex:glossary/sql/join
tags:
- fundamentals
- data-types
- logic
title: 'NULL'
world: sql
---

# NULL

## Definition
In SQL, `NULL` is a special marker used to indicate that a data value does not exist in the database. It represents **missing, unknown, or inapplicable** information. 

> [!IMPORTANT]
> `NULL` is not the same as zero (`0`), an empty string (`''`), or a space. It is the absence of a value entirely.

## Three-Valued Logic
SQL uses "Three-Valued Logic." A comparison can result in `TRUE`, `FALSE`, or `UNKNOWN`.
- Any direct comparison with `NULL` (like `=` or `<>`) results in `UNKNOWN`.
- This means `NULL = NULL` is actually `UNKNOWN`, not `TRUE`.

## Usage
To check for `NULL` values, you must use specific operators:
- **`IS NULL`**: Returns true if the value is missing.
- **`IS NOT NULL`**: Returns true if a value exists.

### Example in Filtering
```sql
-- Find users who haven't provided an email
SELECT * 
FROM users 
WHERE email IS NULL;
```

### Example in Joins
When performing a `LEFT JOIN`, any rows in the left table that have no match in the right table will contain `NULL` for the right table's columns.
```sql
-- Find users who have never placed an order
SELECT users.name
FROM users
LEFT JOIN orders ON users.id = orders.user_id
WHERE orders.id IS NULL;
```

## Pitfalls
- **Math with NULL**: Any arithmetic operation involving `NULL` results in `NULL`. For example, `100 + NULL = NULL`.
- **Aggregate functions**: Most functions like `SUM()` or `AVG()` ignore `NULL` values entirely. `COUNT(*)` counts rows with NULLs, but `COUNT(column)` ignores them.

## Related
- WHERE: Often used with `IS NULL` to filter data.
- JOIN: `LEFT JOIN` and `FULL JOIN` are the most common sources of `NULL` results.