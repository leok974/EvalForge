-- TODO: left join and filter NULLs
SELECT d.name AS department
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.id
WHERE 1 = 0
ORDER BY d.name ASC;
