---
title: INNER JOIN
id: sql/inner-join
---
# INNER JOIN

Returns records that have matching values in both tables.

## Syntax
```sql
SELECT users.name, orders.id 
FROM users 
INNER JOIN orders ON users.id = orders.user_id;
```

## Gotchas
- Rows without matches are excluded.
