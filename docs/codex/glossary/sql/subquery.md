---
title: Subquery
id: glossary/sql/subquery
world: sql
level: intermediate
tags: [fundamentals, queries, analytical]
related:
  - codex:glossary/sql/select
  - codex:glossary/sql/from
  - codex:glossary/sql/cte
---

# Subquery

## Definition
A **Subquery** (or Inner Query) is a query nested inside another SQL query. The results of the subquery are passed to the outer query, which uses them as a filter, a column value, or even a temporary table.

## Why It Matters
Subqueries allow you to answer questions that require multiple steps in a single statement. For example, if you want to find "all users who spent more than the average," you first need a subquery to calculate the average before the main query can filter the users.

## Mental Model
Think of a subquery as a **parenthetical calculation** in math. Just like `(2 + 3) * 4` requires you to solve the part inside the parentheses first, SQL solves the inner subquery first and then plugs that result into the rest of the command.

## Example
```sql
-- Find users who have placed at least one order using an IN subquery
SELECT name
FROM users
WHERE id IN (SELECT user_id FROM orders);
```

## Pitfalls
- **Performance**: Deeply nested subqueries can be slow because the database may have to run them multiple times. In many cases, a `JOIN` or a `CTE` is more efficient.
- **Single Value vs. List**: If your subquery uses `=` (e.g., `WHERE id = (SELECT ...)`), the subquery **must** return exactly one row and one column. If it returns more, the query will fail. Use `IN` if you expect multiple results.

## Related
- SELECT: Subqueries are often used in the SELECT list to create calculated columns.
- FROM: Subqueries in the FROM clause are often called "inline views" and must be aliased.
- CTE: A cleaner, more readable alternative to complex subqueries.
