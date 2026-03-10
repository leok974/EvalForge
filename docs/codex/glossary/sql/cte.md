---
title: CTE (Common Table Expression)
id: glossary/sql/cte
world: sql
level: advanced
tags: [analytical, advanced, syntax]
related:
  - codex:glossary/sql/cte-with
  - codex:glossary/sql/from
  - codex:glossary/sql/subquery
---

# CTE (Common Table Expression)

## Definition
A **Common Table Expression (CTE)** is a temporary result set that you can reference within another `SELECT`, `INSERT`, `UPDATE`, or `DELETE` statement. It is defined using the `WITH` keyword at the beginning of a query.

## Why It Matters
CTEs are primarily used to improve query readability and maintainability. Instead of deeply nested subqueries that are hard to read, a CTE allows you to "name" a temporary result and use it like a regular table later in the query.

## Mental Model
Think of a CTE as a "modular variable" for a query. You define the variable once at the top, and then you can join it or filter it in the main query block.

## Example
```sql
-- Use a CTE to find active users first, then join them to orders
WITH active_users AS (
  SELECT id, name
  FROM users
  WHERE is_active = 1
)
SELECT active_users.name, COUNT(orders.id) AS order_count
FROM active_users
JOIN orders ON active_users.id = orders.user_id
GROUP BY active_users.id;
```

## Pitfalls
- **Scope**: A CTE only exists during the execution of that single query. It is not saved to the database.
- **Recursion**: While CTEs can be recursive (`WITH RECURSIVE`), basic CTEs are non-recursive and cannot reference themselves.

## Related
- WITH: The keyword used to start a CTE.
- FROM: CTEs are most commonly referenced in the FROM clause of a main query.
