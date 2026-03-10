-- Example: Finding events without an associated user_login record
-- This is a standard anti-join across two tables
SELECT e.id, e.event_type
FROM events e
LEFT JOIN user_logins ul ON e.id = ul.user_id
WHERE ul.user_id IS NULL;
