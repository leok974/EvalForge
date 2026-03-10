# Hints: Groups & Filters

## Hint 1 — Basic Grouping
To see the volume per category, you first need to group the products together.
`SELECT category, COUNT(*) as count FROM products GROUP BY category;`

## Hint 2 — Filtering Groups
Unlike individual rows (which use `WHERE`), filtering calculated groups requires the `HAVING` clause.
`HAVING COUNT(*) > 5;`

## Hint 3 — Final Solution
Combine the grouped aggregate with the post-grouping filter to find the high-volume categories.
```sql
SELECT category, COUNT(*) as count
FROM products
GROUP BY category
HAVING COUNT(*) > 5;
```
