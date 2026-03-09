# Hints: High-Value Collections

## Hint 1 — Concept
Use the [GROUP BY](glossary/sql/group-by) clause to bucket rows by their `category`. This should come **after** the [FROM](glossary/sql/from) clause.

## Hint 2 — Aggregating
In your [SELECT](glossary/sql/select) list, you should have the grouping column (`category`) and an aggregate function for the price. Use `AVG(price_cents) AS average_price`.

## Hint 3 — Filtering Groups
To filter based on the result of an aggregate function, you must use [HAVING](glossary/sql/having), not [WHERE](glossary/sql/where).
`HAVING average_price > 5000`
