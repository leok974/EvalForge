---
title: WITH (CTE)
id: glossary/sql/cte-with
world: sql
level: advanced
tags: [syntax, advanced, analytical]
related:
  - codex:glossary/sql/cte
  - codex:glossary/sql/select
---

# WITH (CTE)

## Definition
The `WITH` clause marks the start of a **Common Table Expression (CTE)**. It informs the database that you are defining one or more temporary result sets that will be used in the main query that follows immediately.

## Why It Matters
The `WITH` clause is the grammatical "anchor" that enables readable, modular SQL. It allows you to break a complex problem into smaller, logical steps before combining them.

## Syntax
```sql
WITH [CTE_Name] AS (
  [Your SELECT Query]
),
[Another_CTE] AS (
  [Another Query]
)
SELECT ... FROM [CTE_Name] ...;
```

## Example
```sql
-- Define a CTE to calculate total spent per user
WITH user_spending AS (
  SELECT user_id, SUM(total_cents) AS total_spent
  FROM orders
  GROUP BY user_id
)
SELECT users.name, user_spending.total_spent
FROM users
JOIN user_spending ON users.id = user_spending.user_id;
```

## Pitfalls
- **Trailing Semicolon**: You cannot put a semicolon inside the `WITH` definition; it must only appear at the very end of the entire statement.
- **Comma Placement**: When defining multiple CTEs, use a comma to separate them, but do *not* put a comma after the final one before the main query.

## Related
- CTE: The actual result set created by the WITH clause.
- SELECT: The primary command used inside the WITH clause.
