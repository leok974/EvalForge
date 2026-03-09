# Tutorial: SQL Joins

A [JOIN](glossary/sql/join) clause is used to combine [rows](glossary/sql/row) from two or more [tables](glossary/sql/table), based on a related column between them.

## The INNER JOIN

The most common type of join is the **INNER JOIN**. It returns records that have matching values in both tables.

```sql
SELECT orders.id, users.name
FROM orders
JOIN users ON orders.user_id = users.id;
```

## The ON Clause

Think of the [ON](glossary/sql/on) clause as a bridge. It tells the database which column in Table A matches which column in Table B. These related columns are usually called **Keys**.

-   **Primary Key**: A unique identifier for a row (e.g., `users.id`).
-   **Foreign Key**: A column that references a Primary Key in another table (e.g., `orders.user_id`).

In this quest, you'll bridge the `orders` and `users` tables to reveal the identities behind the transactions.
