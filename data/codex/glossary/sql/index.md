# index

An **index** is a separate data structure that stores pointers to rows in a table. It is used to speed up data retrieval operations (queries) at the cost of slower data writes and additional storage space.

## Analogy

Think of a database index like the index at the back of a physical book. Instead of scanning every page (a "Table Scan"), you look up the term in the alphabetical index and jump straight to the page number.

## Usage

```sql
-- Create an index to speed up searches by email
CREATE INDEX idx_user_email ON users(email);
```

## Trade-offs

- **Pros**: Significantly faster `SELECT` and `ORDER BY` operations on the indexed column.
- **Cons**: Every time you `INSERT`, `UPDATE`, or `DELETE`, the database must also update the index, which adds overhead.
