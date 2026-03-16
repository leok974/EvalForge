# Tutorial: Navigating Complex Schemas

In Tier 2, you learned basic joins. In Tier 3, we deal with "Real Schemas" where data is normalized across many tables.

### 1. Inspect First, Query Second
Open the **Database Explorer** tab. Look at the `employee_assignments` table. Notice it doesn't have names; it only has `employee_id` and `project_id`. This is a **junction table** used to create a many-to-many relationship.

### 2. The Chain of Joins
To get from an Employee to a Project, you must go through the assignment table:
`employees` -> `employee_assignments` -> `projects`

Each JOIN needs an ON clause that matches the keys:
```sql
FROM employees e
JOIN employee_assignments ea ON e.id = ea.employee_id
JOIN projects p ON ea.project_id = p.id
```

### 3. Column Aliasing
When joining tables, column names like `name` often appear in multiple places (e.g., `employees.name` and `projects.name`). Use `AS` to give them unique names in your result set:
```sql
SELECT e.name AS employee_name, p.name AS project_name ...
```

In this mission, you will chain four tables together to generate a high-priority staffing report.
