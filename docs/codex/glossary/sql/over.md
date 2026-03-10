---
id: glossary/sql/over
title: over
world: sql
---

# over

The `OVER` clause is what turns a regular function into a [window function](glossary/sql/window-function). It defines the "window" or range of rows that the function should consider when calculating its value.

## Usage

```sql
SELECT 
  name, 
  RANK() OVER (ORDER BY salary DESC) as rank
FROM employees;
```

## Clauses within OVER

- [PARTITION BY](glossary/sql/partition-by): Divides rows into groups.
- [ORDER BY](glossary/sql/order-by): Sorts rows within the window.
- **ROWS/RANGE**: (Advanced) Defines a specific physical or logical range within the partition.