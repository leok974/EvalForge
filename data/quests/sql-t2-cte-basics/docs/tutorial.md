# Tutorial: CTE Basics (WITH Clause)

As your SQL queries become more complex, they can become difficult to read. A **Common Table Expression (CTE)** allows you to define a temporary result set that you can reference within another query.

## The WITH Clause

The `WITH` clause defines a CTE. You can think of it as creating a temporary [table](glossary/sql/table) that only exists for the duration of the query.

```sql
WITH MyTemporaryTable AS (
  SELECT name, salary
  FROM employees
  WHERE salary > 100000
)
SELECT * FROM MyTemporaryTable;
```

## Why use CTEs?

1. **Readability**: It breaks a long query into logical blocks.
2. **Reuse**: You can reference the CTE multiple times in the main query.
3. **Debugging**: You can test the CTE logic independently before combining it.

## Logical Order

A CTE must always be defined **before** the main `SELECT` statement:

1. **WITH**: Define the temporary view.
2. **SELECT**: Use the view.

In this quest, you will use a CTE to first count events by type, and then filter those counts in the final output.
