# Mission: UPSERT (ON CONFLICT)
**Goal**: 
Insert into `user_logins (user_id, login_count, last_login)` values `(1, 1, '2023-10-10')`.
If there is a conflict on `user_id` (PRIMARY KEY), update the existing row:
- Add 1 to `login_count` (`login_count = login_count + 1`)
- Update `last_login` to `excluded.last_login`
Return all rows from `user_logins` ordered by `user_id` ASC.