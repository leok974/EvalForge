# and

The `AND` operator is used in a [WHERE](glossary/sql/where) clause to combine two or more conditions. It returns rows only if **all** the conditions are true.

## Usage

```sql
SELECT * FROM users
WHERE city = 'Detroit' AND is_active = 1;
```

In this example, a user will only be returned if they live in Detroit AND are currently active.
