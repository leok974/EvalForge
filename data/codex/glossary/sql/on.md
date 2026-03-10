# on

The `ON` keyword is used with `JOIN` to specify the relationship between two tables—usually matching a primary key in one table to a foreign key in another.

## Usage

```sql
SELECT *
FROM orders
JOIN customers ON orders.customer_id = customers.id;
```

The `ON` clause acts like a filter specifically for the relationship between the two tables.
