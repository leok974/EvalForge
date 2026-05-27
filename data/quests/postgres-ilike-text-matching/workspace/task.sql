-- Starter code for ILIKE quest
-- We need to find all employees with an '@example.com' email address.
-- Some emails might be capitalized inconsistently (e.g., '@Example.com').
-- Fill in the WHERE clause below.

SELECT id, name, email 
FROM employees
WHERE -- TODO: match the @example.com domain case-insensitively
