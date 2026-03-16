# Skill Matrix

The head of Engineering needs a flat report of all technical skills the department possesses. 

Currently, the `skills` column in the `employees` table is a PostgreSQL Array (`TEXT[]`). If you just select it, you get grouped arrays back.

Your task is to write a query that returns the employee `name` and their individual `skills`, unnested so there is only one skill per row.

Make sure you only return employees in the Engineering department (`department_id = 1`).
