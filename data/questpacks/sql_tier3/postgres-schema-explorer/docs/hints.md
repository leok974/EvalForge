# Mission Hints: Schema Exploration

Need a hand navigating the archives? Use these gated hints to guide your tactical approach.

## Hint 1 — Look at the Metadata
The **Database Explorer** is your primary tool. Click on the `employees` table in the sidebar to see the available columns and their types.

## Hint 2 — Resolving the Department
The `employees` table has a `department_id` rather than a text-based department name. To filter by `'Engineering'`, you'll need to look at the `departments` table first to find the corresponding `id`.

## Hint 3 — Subqueries vs Joins
You can either use a `JOIN` to bring the tables together, or a subquery like `WHERE department_id = (SELECT id FROM departments WHERE name = 'Engineering')`. Choosing the right approach depends on the scale of your data!
