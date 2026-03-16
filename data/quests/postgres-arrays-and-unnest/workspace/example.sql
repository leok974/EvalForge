-- Example: Finding a specific skill in an array
SELECT name, email, skills
FROM employees
WHERE 'Postgres' = ANY(skills);
