-- sql-t2-upsert-on-conflict
-- TASK:
-- Record a user login. Increment the count if the user exists.
--
-- Output columns (exact order):
--   user_id, login_count, last_login
--
-- Rules:
-- - Insert user_id=1, login_count=1, last_login='2023-10-10'
-- - On conflict(user_id), increment existing login_count by 1
-- - On conflict(user_id), update last_login to excluded value
-- - Include final SELECT * FROM user_logins
--
-- TODO:
-- Update the query below to handle the unique constraint conflict.

INSERT INTO user_logins (user_id, login_count, last_login)
VALUES (1, 1, '2023-10-10');
-- TODO: Add ON CONFLICT(...) DO UPDATE

SELECT * FROM user_logins ORDER BY user_id ASC;
