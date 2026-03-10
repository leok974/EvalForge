# asc

`ASC` (short for "Ascending") is a keyword used in the `ORDER BY` clause to sort data from lowest to highest (e.g., A to Z, or 1 to 100).

## Usage

```sql
-- Sort users alphabetically
SELECT * FROM users ORDER BY name ASC;
```

In most databases (including SQLite), **Ascending is the default**. If you don't specify `ASC` or `DESC`, the database will use `ASC`.
