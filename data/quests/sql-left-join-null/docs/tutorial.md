# Tutorial: Left Joins & NULLs

An `INNER JOIN` only returns rows where there is a match in both [tables](glossary/sql/table). But what if you want to see *all* records from one table, regardless of whether they have a match in the other?

## The LEFT JOIN

A **[LEFT JOIN](glossary/sql/join)** returns all records from the left table (the first one mentioned), and the matched records from the right table. If there is no match, the result is **[NULL](glossary/sql/null)** on the right side.

```sql
SELECT users.name, orders.id
FROM users
LEFT JOIN orders ON users.id = orders.user_id;
```

In the result above, any user who hasn't ordered anything will have a `NULL` in the `orders.id` column.

## Finding the "Missing" Data

By combining a `LEFT JOIN` with a [WHERE](glossary/sql/where) clause that checks for `NULL`, you can find exactly which records are "missing" a relationship.

```sql
SELECT users.name
FROM users
LEFT JOIN orders ON users.id = orders.user_id
WHERE orders.id IS NULL;
```

This is a powerful pattern for finding inactive users, unsold products, or empty categories.
