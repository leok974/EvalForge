-- Example: Simple recursion for numbers
-- This generates a sequence of numbers from 1 to 5
WITH RECURSIVE counter(n) AS (
  SELECT 1
  UNION ALL
  SELECT n + 1 FROM counter WHERE n < 5
)
SELECT n FROM counter;
