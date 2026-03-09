# Hints: Filter the Data

## Hint 1 — Concept
Use the [WHERE](glossary/sql/where) clause to restrict which rows are returned. Place it **after** the [FROM](glossary/sql/from) clause but **before** the [ORDER BY](glossary/sql/order-by) clause.

## Hint 2 — Multiple Conditions
To filter by two things at once (like city and active status), use the `AND` keyword.
`WHERE city = 'Detroit' AND is_active = 1`

## Hint 3 — The Full Query
Your final query should look something like this:
```sql
SELECT name, age, city
FROM users
WHERE city = 'Detroit' AND is_active = 1
ORDER BY name ASC;
```

Expected: 4 rows — Alice (Detroit), Bob (Austin), Diana (Seattle), Fay (Miami).
*(Note: These are examples, your actual results will depend on the seeded data for Detroit specifically.)*
