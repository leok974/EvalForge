# Multi-Table JOINs

A JOIN combines rows from two tables based on a matching key.

## Basic syntax

```sql
SELECT a.col, b.col
FROM table_a a
JOIN table_b b ON a.foreign_key = b.id;
```

## Chaining multiple JOINs

You can chain JOINs to traverse a relationship graph:

```sql
SELECT e.name, d.name, p.name
FROM employee_assignments ea
JOIN employees e    ON ea.employee_id   = e.id
JOIN departments d  ON e.department_id  = d.id
JOIN projects p     ON ea.project_id    = p.id;
```

Each JOIN adds one more table to the result. Work left-to-right: start with the junction table (employee_assignments), then join outward to the entities it references.

## Filtering after JOINs

Add a WHERE clause after all JOIN clauses to filter rows:

```sql
WHERE p.budget > 50000
```

## Column aliases

Use AS to rename columns in the output:

```sql
e.name AS employee_name,
d.name AS department_name
```

This makes the result readable even when multiple tables have columns with the same name.
