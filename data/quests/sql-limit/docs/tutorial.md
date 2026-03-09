# Tutorial: The LIMIT Clause

`LIMIT` tells SQL to return only the first **N rows** from the result set.

That sounds simple, but there is an important catch: without an `ORDER BY`, SQL is free to return rows in whatever order the database happens to produce them. That means `LIMIT 3` by itself does **not** reliably mean “top 3” or “first 3 alphabetically.”

## The Standard Pipeline

The usual pattern for a "Top N" report is:

```sql
SELECT ...
FROM ...
WHERE ...
ORDER BY ...
LIMIT N;
```

Think of it as a three-step pipeline:

1.  **Filter**: Use `WHERE` to include only the rows you care about (e.g., active products).
2.  **Sort**: Use `ORDER BY` to put them in the desired order (e.g., price descending).
3.  **Trim**: Use `LIMIT` to cap the result to a specific number of rows.

## Why Order Matters

Imagine you have a list of all students and you want the "top 3 by grade." If you forget `ORDER BY grade DESC`, the database might just hand you the first 3 students it found in its files, regardless of their grades.

In this quest, you are not just returning products — you are returning the **top 3 most expensive active products**.
