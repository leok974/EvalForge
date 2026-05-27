# Mission Hints: Schema Exploration

Need a hand navigating the archives? Use these gated hints to guide your tactical approach.

## Hint 1 — Look at the Metadata
The **Database Explorer** is your primary tool. Click on the `employees` table in the sidebar to see the available columns. You'll notice it has a `department_id` instead of a department name.

## Hint 2 — Resolving the Department
The `departments` table contains the link you need. Look for a column that maps an `id` to a `name`. You'll need to find the `id` corresponding to `'Engineering'`.

## Hint 3 — Implementation
You can use a **Subquery** to solve this cleanly. Try:
`WHERE department_id = (SELECT id FROM departments WHERE name = 'Engineering')`.
This avoids a complex join while providing the exact filter needed.
