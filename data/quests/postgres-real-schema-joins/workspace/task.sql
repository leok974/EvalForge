-- Mission: List all employees assigned to projects with a budget greater than $50,000.
-- Return the employee name, their department name, the project name, and their role.
-- Alias the columns as: employee_name, department_name, project_name, role.

SELECT 
    e.name AS employee_name,
    d.name AS department_name,
    p.name AS project_name,
    ea.role
FROM employees e
JOIN departments d ON e.department_id = d.id
JOIN employee_assignments ea ON e.id = ea.employee_id
-- JOIN projects p ... (Complete the join and filter)
WHERE p.budget > 50000;
