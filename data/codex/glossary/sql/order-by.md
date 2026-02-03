---
title: ORDER BY
id: sql/order-by
---
# ORDER BY

Sorts the result set in ascending or descending order.

## Syntax
```sql
SELECT * FROM users ORDER BY name ASC;
```

## Options
- `ASC`: Ascending (default)
- `DESC`: Descending

## Gotchas
- Sorting by multiple columns: `ORDER BY col1, col2 DESC`.
