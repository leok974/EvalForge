# Hints: UPSERT & ON CONFLICT

## Hint 1 — The Clause
To handle a duplicate key error gracefully, use the `ON CONFLICT` clause followed by the unique column.
`ON CONFLICT(user_id)`

## Hint 2 — Updating
If a conflict occurs, you want to perform an update. Use `DO UPDATE SET`.
`DO UPDATE SET login_count = user_logins.login_count + 1`

## Hint 3 — The Excluded Table
To reference the values you *tried* to insert (like the new date), use the special `excluded` table.
`last_login = excluded.last_login`

## Hint 4 — The Full Query
```sql
INSERT INTO user_logins (user_id, login_count, last_login) 
VALUES (1, 1, '2023-10-10') 
ON CONFLICT(user_id) 
DO UPDATE SET 
    login_count = user_logins.login_count + 1, 
    last_login = excluded.last_login;

SELECT * FROM user_logins ORDER BY user_id ASC;
```
