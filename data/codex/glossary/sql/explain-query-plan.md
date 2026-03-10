# explain-query-plan

The `EXPLAIN QUERY PLAN` command is used to see the internal strategy the database engine uses to execute a query. It is the primary tool for performance profiling in SQL.

## Usage

Prefix any `SELECT`, `INSERT`, `UPDATE`, or `DELETE` statement with the command:

```sql
EXPLAIN QUERY PLAN
SELECT * FROM users WHERE email = 'alice@example.com';
```

## Reading the Output

Common phrases you might see:
- **SCAN TABLE**: The database had to check every single row. This is slow for large tables.
- **SEARCH TABLE ... USING INDEX**: The database used an [index](glossary/sql/index) to jump straight to the correct data. This is fast!
- **USE TEMP B-TREE**: The database had to create a temporary internal data structure, often for a complex `ORDER BY` or `JOIN`.
