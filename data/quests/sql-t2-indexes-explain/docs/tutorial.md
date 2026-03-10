# Tutorial: Indexes & EXPLAIN QUERY PLAN

As your database grows from hundreds to millions of rows, simple queries can become slow. To speed them up, you use **Indexes**.

## What is an Index?

An **index** is like the index at the back of a book. Instead of reading every page (a "Full Table Scan") to find a specific word, you look at the index to find the exact page number and jump straight there.

In SQL, you create an index on a specific column that you frequently use for filtering (`WHERE`) or joining.

```sql
CREATE INDEX idx_user_email ON users(email);
```

## EXPLAIN QUERY PLAN

How do you know if your index is actually working? You use the `EXPLAIN QUERY PLAN` command. It tells you the steps the database will take to execute your query.

- **SEARCH**: Good! This means the database is using an index to jump to the data.
- **SCAN**: Slow! This means the database is reading every single row in the table.

```sql
EXPLAIN QUERY PLAN 
SELECT * FROM users WHERE email = 'alice@example.com';
```

In this quest, you will create an index to speed up manager lookups and verify its usage by inspecting the query plan.
