---
id: glossary/sql/max
title: max
world: sql
---

# max

`MAX()` is an aggregate function that returns the largest value of the selected column.

## Usage

```sql
-- Find the highest salary in the company
SELECT MAX(salary) FROM employees;
```

`MAX()` works on numbers, strings (Z is higher than A), and dates (the most recent date is the highest).