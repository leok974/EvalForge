---
title: LEFT JOIN
id: sql/left-join
---
# LEFT JOIN

Returns all records from the left table, and matched records from the right table.

## Syntax
```sql
SELECT users.name, orders.id 
FROM users 
LEFT JOIN orders ON users.id = orders.user_id;
```

## Result
- If no match, right side columns are `NULL`.
