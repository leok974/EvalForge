# sum

`SUM()` is an aggregate function that returns the total sum of a numeric column.

## Usage

```sql
-- Find total revenue from all orders
SELECT SUM(amount) FROM orders;

-- Find total revenue per category
SELECT category, SUM(amount)
FROM sales
GROUP BY category;
```

`SUM()` ignores [NULL](glossary/sql/null) values.
