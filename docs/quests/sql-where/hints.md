# Hints: Filter the Data

## Hint 1 — Concept
Use the `WHERE` clause to restrict which rows are returned. Place it **after** `FROM` and **before** `ORDER BY`.

## Hint 2 — Structure

```sql
SELECT id, name, city
FROM users
WHERE ___
ORDER BY name ASC;
```

Fill in the blank: what condition filters out inactive users?

## Hint 3 — Full solution

```sql
SELECT id, name, city
FROM users
WHERE is_active = 1
ORDER BY name ASC;
```

Expected: 4 rows — Alice (Detroit), Bob (Austin), Diana (Seattle), Fay (Miami).
