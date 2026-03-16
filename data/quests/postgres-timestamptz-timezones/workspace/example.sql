-- Example: Converting to different Timezones using AT TIME ZONE

-- 1. Seeing the UTC time
SELECT name, hired_at
FROM employees;

-- 2. Converting to Pacific Time (PST/PDT)
SELECT name, hired_at AT TIME ZONE 'America/Los_Angeles' AS pt_hired_at
FROM employees;

-- 3. Converting to Central European Time (CET/CEST)
SELECT name, hired_at AT TIME ZONE 'Europe/Berlin' AS cet_hired_at
FROM employees;
