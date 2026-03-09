# Tutorial: Grouped Analytics

In the previous quest, we "squished" the entire table into one row. But what if you want a summary row for every category? That's where **[GROUP BY](glossary/sql/group-by)** comes in.

## How GROUP BY Works

When you use [GROUP BY](glossary/sql/group-by), you tell [SQL](glossary/sql/select) to create buckets based on a column. Any [aggregate functions](glossary/sql/count) in your [SELECT](glossary/sql/select) list will then be calculated once for every bucket.

```sql
SELECT city, COUNT(*)
FROM users
GROUP BY city;
```

This query would show you how many users live in each city.

## Filtering Groups with HAVING

There is a catch: you cannot use [WHERE](glossary/sql/where) to filter based on an aggregate result. This is because [WHERE](glossary/sql/where) filters rows *before* they are grouped.

If you want to filter *after* grouping, you must use **[HAVING](glossary/sql/having)**.

```sql
SELECT city, COUNT(*) AS user_count
FROM users
GROUP BY city
HAVING user_count > 1;
```

In this quest, you will group by category and use `HAVING` to filter for premium price points.
