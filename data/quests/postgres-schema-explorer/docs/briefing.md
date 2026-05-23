## Overview
Welcome to the **Deep Archives**, a region of space where history is stored in high-performance **PostgreSQL** instances. Unlike the immutable blocks of the Core Worlds, this environment requires active **Schema Exploration** and precision querying.

## Mission
Your objective is to locate all personnel assigned to the **Engineering** department within the `archives` database. You must provide their contact details for a critical integrity audit.

## Requirements
- Use the **Database Explorer** to identify the structure of `employees` and `departments`.
- Return exactly two columns: `name` and `email`.
- Filter results to only include employees in the `'Engineering'` department.
- Order the final list alphabetically by `name`.

## Suggested Workflow
1. Open the **Database** tab in the left pane.
2. Expand the `public` schema and inspect the `employees` table.
3. Check the `departments` table to see how the name `'Engineering'` matches.
4. Draft your query in `task.sql`.
5. Run your query to verify the output matches the audit requirements.

## Watch For
The `employees` table uses a `department_id` foreign key. You must resolve the department name correctly, potentially using a subquery or a `JOIN`.
