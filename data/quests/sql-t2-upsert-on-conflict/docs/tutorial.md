# Tutorial: UPSERT & ON CONFLICT

In many applications, you want to [INSERT](glossary/sql/insert) a new [row](glossary/sql/row), but if that row already exists (based on a unique ID), you want to [UPDATE](glossary/sql/update) the existing one instead. This pattern is called an **UPSERT** (Update or Insert).

## The Problem: Unique Constraints

If you try to `INSERT` a row with an ID that already exists in the table, the database will throw a "Unique Constraint Violation" error and stop the query.

## The Solution: ON CONFLICT

SQLite provides the `ON CONFLICT` clause to handle these errors gracefully.

```sql
INSERT INTO user_logins (user_id, login_count)
VALUES (1, 1)
ON CONFLICT(user_id) 
DO UPDATE SET login_count = user_logins.login_count + 1;
```

### Breakdown:
1. **`ON CONFLICT(user_id)`**: Specifies which column has the unique constraint you are checking.
2. **`DO UPDATE SET ...`**: Tells SQL what to do if a conflict is found.
3. **`excluded` Keyword**: You can use the special `excluded` table to reference the values you *tried* to insert. For example, `last_login = excluded.last_login` would take the date from your failed INSERT and apply it to the existing row.

In this quest, you will perform an UPSERT that increments a login counter and updates the last login timestamp for an existing user.
