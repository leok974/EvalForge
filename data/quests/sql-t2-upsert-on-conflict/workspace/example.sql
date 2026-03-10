-- Example: Simple UPSERT for a guest
-- This inserts a guest session or updates the visit count
INSERT INTO user_logins (user_id, login_count, last_login) 
VALUES (999, 1, '2023-10-01')
ON CONFLICT(user_id) 
DO UPDATE SET login_count = login_count + 1;

SELECT * FROM user_logins WHERE user_id = 999;
