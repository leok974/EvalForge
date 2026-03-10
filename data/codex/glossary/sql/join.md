# join

The `JOIN` clause is used to combine rows from two or more tables based on a related column between them.

## Common Types

- **INNER JOIN**: Returns rows only when there is a match in both tables.
- **LEFT JOIN**: Returns all rows from the left table, and matched rows from the right. Unmatched rows on the right show as `NULL`.
- **CROSS JOIN**: Returns every possible combination of rows from both tables.

## Usage

```sql
SELECT users.name, orders.amount
FROM users
JOIN orders ON users.id = orders.user_id;
```
