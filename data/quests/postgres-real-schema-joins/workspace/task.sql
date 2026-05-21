-- Quest: postgres-real-schema-joins
-- Goal: JOIN across 4 tables to find employees, their departments,
--       their projects, and their roles — only for high-budget projects.

SELECT
    e.name  AS employee_name,
    d.name  AS department_name,
    p.name  AS project_name,
    ea.role
FROM employee_assignments ea
-- TODO: JOIN the employees table so you can get employee names
-- TODO: JOIN the departments table so you can get department names
-- TODO: JOIN the projects table so you can get project name and budget
-- TODO: filter to only include projects where budget > 50000
ORDER BY employee_name;
