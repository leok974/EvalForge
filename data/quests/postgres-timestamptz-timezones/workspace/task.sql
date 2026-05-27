-- Starter code for TIMESTAMPTZ quest
-- The `hired_at` column is stored in UTC because it's a TIMESTAMPTZ.
-- However, HR wants to know the local hiring time for our Tokyo office.
-- 
-- Convert `hired_at` to the 'Asia/Tokyo' timezone.
-- Return name, email, and the local_hired_at time.

SELECT name, email,
       -- TODO: convert `hired_at` to 'Asia/Tokyo' timezone
FROM employees;
