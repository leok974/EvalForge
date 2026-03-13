---
id: glossary/sql/inner-join
title: INNER JOIN
world: sql
---

# INNER JOIN

`INNER JOIN` is the most common type of join. It returns only the rows where there is a match in both the joined tables.

## How it works

If a row in Table A does not have a corresponding match in Table B (based on the join condition), that row will not appear in the final result set.

## Basic Syntax

```sql
SELECT a.column, b.column
FROM table_a a
INNER JOIN table_b b ON a.common_id = b.a_id;
```

## Example

Link employees to their departments:
```sql
SELECT e.name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id;
```
If an employee is not assigned to a department, they will be excluded from this list.
