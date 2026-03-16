-- Starter code for Arrays & Unnest quest
-- Look at the `skills` column in `employees`. It's a TEXT[] array!
-- We need a flat list of every single skill our engineers have, alongside their name.
-- Use the UNNEST() function to flatten the `skills` array.

SELECT name, -- TODO: unnest the skills array here
FROM employees
WHERE department_id = 1; -- Just the Engineering department
