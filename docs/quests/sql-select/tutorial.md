# SQL Select — Directory Query

## Task
Edit `task.sql` to return a directory of users.

### Output (exact)
Return columns in this order:

1) `name`  
2) `city`

### Rules
- Source: `users`
- Include all rows (no WHERE needed)
- Sort: `ORDER BY name ASC`

## Schema
Table: `users`
Columns: `id, name, email, age, city, is_active`

## How to verify
Click **Run** → open **Query Result**.
- Check the column order is `name, city`
- Check it’s sorted alphabetically by `name`
