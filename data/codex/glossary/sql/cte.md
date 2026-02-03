---
title: Common Table Expressions (CTE)
id: sql/cte
---
# CTE

A temporary result set named within the execution scope of a statement.

## Syntax
```sql
WITH regional_sales AS (
    SELECT region, SUM(amount) as total_sales
    FROM orders
    GROUP BY region
)
SELECT * FROM regional_sales WHERE total_sales > 1000;
```
