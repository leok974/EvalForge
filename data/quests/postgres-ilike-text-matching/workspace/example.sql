-- Example: Using ILIKE for case-insensitive matching
-- Notice how ILIKE matches 'Admin', 'admin', 'ADMIN', etc.
-- Compare this to how strict the '=' operator is.

SELECT name, email
FROM employees
WHERE name ILIKE '%admin%';
