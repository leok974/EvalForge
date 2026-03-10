---
id: glossary/sql/table
level: beginner
related:
- codex:glossary/sql/column
- codex:glossary/sql/row
tags:
- sql
- fundamentals
title: Table
world: sql
---

# Table

A **Table** is the fundamental building block of a relational database. It stores related data in a grid-like structure consisting of horizontal **Rows** and vertical **Columns**.

## Why It Matters
Tables provide the structure necessary for efficient querying. By separating "Employees" from "Departments" into different tables (Normalization), we avoid data duplication and ensure that updates are consistent.

## Components
- **Column**: A vertical entity that represents a specific attribute (e.g., `first_name`, `hire_date`). Each column has a defined **Data Type**.
- **Row (Record)**: A horizontal entity representing a single item in the table (e.g., one specific employee).
- **Primary Key**: A column (or set of columns) that uniquely identifies each row in the table.

## Syntax Example
```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    hire_date DATE DEFAULT CURRENT_DATE
);
```

To see the content of a table:
```sql
SELECT * FROM employees LIMIT 10;
```

## Common Mistake
Failing to define a **Primary Key**. Without a unique identifier, it becomes extremely difficult to update or delete specific records safely.