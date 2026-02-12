SELECT d.name AS department
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.id
WHERE e.id IS NULL
ORDER BY d.name ASC;
