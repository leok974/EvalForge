---
title: Subquery
id: sql/subquery
---
# Subquery

A query nested inside another query.

## Syntax
```sql
SELECT * FROM products 
WHERE price > (SELECT AVG(price) FROM products);
```

## Types
- Scalar subquery (returns one value)
- Table subquery (returns rows/cols)
