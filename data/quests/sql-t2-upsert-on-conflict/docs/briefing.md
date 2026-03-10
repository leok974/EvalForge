**Quest: UPSERT & ON CONFLICT**

### The Mission
A user just logged in! We need to record this activity. If the user is new, we should create a record. If they've logged in before (the `user_id` already exists), we should increment their `login_count` and update their `last_login` timestamp.

Perform a safe [upsert](glossary/sql/upsert) for `user_id = 1`.

### Requirements
1. **Operation**: Perform an `INSERT` into the `user_logins` table for `user_id = 1`, with a `login_count` of `1` and a `last_login` of `'2023-10-10'`.
2. **Handle Conflict**: 
   - Use [ON CONFLICT](glossary/sql/on-conflict) on the `user_id` column.
   - If a conflict occurs, `DO UPDATE` the existing record.
   - Increment the existing `login_count` by 1.
   - Update `last_login` to the new value (use the `excluded.last_login` reference).
3. **Verification**: After your UPSERT statement, include a `SELECT * FROM user_logins ORDER BY user_id ASC;` to show the final state.
