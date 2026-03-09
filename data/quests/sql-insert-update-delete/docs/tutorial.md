# Tutorial: Data Mutation (DML)

Data Manipulation Language (DML) is the subset of [SQL](glossary/sql/select) used for adding, changing, and deleting data.

## INSERT: Adding Data

To add a new [row](glossary/sql/row) to a [table](glossary/sql/table), use **[INSERT INTO](glossary/sql/insert)**. You must specify the table, the columns, and the values.

```sql
INSERT INTO users (id, name, age)
VALUES (7, 'Grace', 30);
```

## UPDATE: Changing Data

To modify existing records, use **[UPDATE](glossary/sql/update)**. **WARNING**: Always use a [WHERE](glossary/sql/where) clause with `UPDATE`, or you will change every single row in the table!

```sql
UPDATE users
SET city = 'London'
WHERE id = 2;
```

## DELETE: Removing Data

To remove records, use **[DELETE FROM](glossary/sql/delete)**. Like `UPDATE`, you must specify a [WHERE](glossary/sql/where) clause to avoid deleting everything.

```sql
DELETE FROM orders
WHERE id = 4;
```

In this quest, you will perform all three operations to keep the Archive current.
