# Tutorial: The WHERE Clause

In SQL, the [SELECT](glossary/sql/select) and [FROM](glossary/sql/from) clauses define *what* columns you want and *where* they come from. But often, you don't want every single [row](glossary/sql/row) in the [table](glossary/sql/table).

The [WHERE](glossary/sql/where) clause allows you to **filter** data based on specific conditions.

## Basic Syntax

```sql
SELECT column1, column2
FROM table_name
WHERE condition;
```

The condition is a boolean expression that must be true for a row to be included in the final [result set](glossary/sql/select).

## Common Operators

-   **Equals (`=`)**: Matches an exact value. Strings must be enclosed in single quotes (e.g., `city = 'Detroit'`).
-   **Not Equals (`<>` or `!=`)**: Matches anything except the value.
-   **Comparison (`>`, `<`, `>=`, `<=`)**: Used for numbers or dates.
-   **Logical [AND](glossary/sql/and)**: Combines two conditions; both must be true.
-   **Logical OR**: Combines two conditions; at least one must be true.

## Order of Operations

In a standard query, the [WHERE](glossary/sql/where) clause always comes **after** [FROM](glossary/sql/from) and **before** [ORDER BY](glossary/sql/order-by).

```sql
SELECT name, city
FROM users
WHERE is_active = 1
ORDER BY name ASC;
```

In this quest, you'll need to use the `AND` operator to filter by both `city` and `is_active` status.
