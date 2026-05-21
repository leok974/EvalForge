SELECT
    e.name  AS employee_name,
    d.name  AS department_name,
    p.name  AS project_name,
    ea.role
FROM employee_assignments ea
JOIN employees e  ON ea.employee_id = e.id
JOIN departments d ON e.department_id = d.id
JOIN projects p   ON ea.project_id   = p.id
WHERE p.budget > 50000
ORDER BY employee_name;
