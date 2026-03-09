# Tutorial: SQL Aggregates

Normally, [SQL](glossary/sql/select) returns one row for every row it finds in the [table](glossary/sql/table). But sometimes, you want to "squish" all those rows into a single summary row. This is where **Aggregate Functions** come in.

## Common Aggregate Functions

-   **[COUNT](glossary/sql/count)**: Counts the number of rows. `COUNT(*)` counts everything.
-   **[SUM](glossary/sql/sum)**: Adds up the values in a numeric column.
-   **[AVG](glossary/sql/avg)**: Calculates the average value of a numeric column.
-   **[MIN](glossary/sql/min)** / **[MAX](glossary/sql/max)**: Finds the smallest or largest value.

## Naming Your Results (Aliasing)

When you use an aggregate function, the database doesn't always know what to name the output column. You can use the `AS` keyword to give it a clean name.

```sql
SELECT COUNT(*) AS total_items
FROM products;
```

In this quest, you'll use both `COUNT` and `SUM` in the same [SELECT](glossary/sql/select) statement to summarize your inventory.
