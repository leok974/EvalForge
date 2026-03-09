# Hints: Counting and Adding

## Hint 1 — Concept
Use the aggregate functions [COUNT](glossary/sql/count) and [SUM](glossary/sql/sum) in your [SELECT](glossary/sql/select) clause.

## Hint 2 — Aliasing
To name your columns correctly, use the `AS` keyword. For example: `COUNT(*) AS total_count`.

## Hint 3 — The Answer
Your query should look something like this:
```sql
SELECT
  COUNT(*) AS total_count,
  SUM(price_cents) AS total_value_cents
FROM products;
```
This will produce a single row summarizing the entire table.
