# Tutorial: CTEs & Subqueries

When you need to use the result of one query inside another, you have two main choices: **Subqueries** or **[CTEs](glossary/sql/cte)**.

## What is a CTE?

A **Common Table Expression (CTE)** is a temporary result set that you can reference within a [SELECT](glossary/sql/select), INSERT, UPDATE, or DELETE statement. You define it using the `WITH` clause.

```sql
WITH regional_data AS (
  SELECT * FROM users WHERE city = 'Detroit'
)
SELECT name FROM regional_data;
```

Think of a [CTE](glossary/sql/cte) as a "named subquery" that makes your code much easier to read and maintain.

## Why use CTEs?

-   **Readability**: They allow you to define parts of your query at the top, like variables.
-   **Debugging**: You can test the [CTE](glossary/sql/cte) independently before using it in a complex join.
-   **Recursion**: Certain advanced queries (like finding all children in a hierarchy) require [CTEs](glossary/sql/cte).

In this quest, you'll use a [CTE](glossary/sql/cte) to "pre-filter" your data before calculating total spend.
