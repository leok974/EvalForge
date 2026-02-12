SELECT e.name AS employee, d.name AS department
FROM employees e
JOIN departments d ON d.id = e.dept_id
ORDER BY e.id ASC;
