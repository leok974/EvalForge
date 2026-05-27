SELECT 
    e.name,
    e.email,
    d.name as department
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE d.name = 'Engineering'
ORDER BY e.name;
