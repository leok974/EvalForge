# count

`COUNT()` is an aggregate function that returns the total number of rows that match a specified criterion.

## Variations

- **COUNT(*)**: Counts every row, including those with `NULL` values.
- **COUNT(column_name)**: Counts only the rows where the specified column is NOT `NULL`.
- **COUNT(DISTINCT column_name)**: Counts only the [unique](glossary/sql/unique) non-null values.

## Usage

```sql
-- Find total number of users
SELECT COUNT(*) FROM users;

-- Find number of users with a secondary email
SELECT COUNT(secondary_email) FROM users;
```
