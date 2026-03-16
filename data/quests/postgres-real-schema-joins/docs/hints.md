# Hints: PostgreSQL Joins

## Hint 1 — Joining the Junction
You need to link `employees` to `employee_assignments` using `e.id = ea.employee_id`. Then, link `employee_assignments` to `projects` using `ea.project_id = p.id`.

## Hint 2 — The Department Link
Don't forget to join `departments` using `e.department_id = d.id` to get the department name.

## Hint 3 — Filtering
The `WHERE` clause should target `p.budget`. Remember to use a numeric comparison without commas or dollar signs.
