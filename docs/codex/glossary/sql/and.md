---
title: AND
id: glossary/sql/and
world: sql
level: beginner
tags: [fundamentals, syntax, filtering]
related:
  - codex:glossary/sql/where
  - codex:glossary/sql/row
---

# AND

## Definition
The `AND` operator is used to filter records based on **multiple conditions**. For a row to be included in the result set, it must satisfy all the conditions separated by `AND`.

## Why It Matters
`AND` allows you to be much more specific with your queries. Instead of just searching for users in "Austin," you can search for users who are in "Austin" **AND** have an "active" account status.

## Syntax
```sql
SELECT ... FROM ...
WHERE condition1 AND condition2 AND ...;
```

## Example
```sql
-- Find active users who live in Detroit
SELECT name, email
FROM users
WHERE city = 'Detroit' AND is_active = 1;
```

## Pitfalls
- **Conflicting Conditions**: If you use `AND` with two conditions that cannot both be true (e.g., `city = 'Austin' AND city = 'Detroit'`), the query will return zero results.
- **Operator Precedence**: When mixing `AND` with `OR`, always use parentheses to clarify your logic, as `AND` is usually processed before `OR`.

## Related
- WHERE: The clause that most commonly uses the AND operator.
- Row: Individual data entries that must pass all AND conditions to be selected.
