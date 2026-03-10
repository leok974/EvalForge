-- Example: Using a CTE to find high earners
WITH HighEarners AS (
  SELECT name, salary
  FROM employees
  WHERE salary > 120000
)
SELECT name FROM HighEarners ORDER BY name;
