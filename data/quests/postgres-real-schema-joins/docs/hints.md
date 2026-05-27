## Hint 1
Start from the junction table: `FROM employee_assignments ea`. It connects employees to projects via `employee_id` and `project_id` foreign keys.

## Hint 2
Chain three JOINs: one to `employees` (for name and department_id), one to `departments` (for department name), one to `projects` (for project name and budget).

## Hint 3
Filter with `WHERE p.budget > 50000` after all JOIN clauses. Use `ORDER BY employee_name` to sort alphabetically.
