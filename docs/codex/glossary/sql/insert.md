---
id: glossary/sql/insert
title: insert
world: sql
---

# insert

The `INSERT INTO` statement is used to add new rows of data to a table.

## Usage

```sql
INSERT INTO users (name, email) 
VALUES ('Alice', 'alice@example.com');
```

If you are inserting data into every column in the correct order, you can omit the column names:

```sql
INSERT INTO users 
VALUES (1, 'Alice', 'alice@example.com', 1);
```