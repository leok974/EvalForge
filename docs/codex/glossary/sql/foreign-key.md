---
id: glossary/sql/foreign-key
title: Foreign Key
world: sql
---

# Foreign Key

A **Foreign Key** is a column (or group of columns) in one table that points to the **Primary Key** in another table. It is the fundamental mechanism for creating relationships between data in a relational database.

## Critical Concepts

1. **Referential Integrity**: Ensures that you cannot have a value in the foreign key column that doesn't exist in the parent table.
2. **Relationships**: Defines how entities (like `Orders` and `Customers`) are linked together.

## Basic Syntax

Creating a table with a foreign key:
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    amount NUMERIC
);
```

## Example

In the relational wave, the `employee_assignments` table uses foreign keys to link `employee_id` to the `employees` table and `project_id` to the `projects` table.
