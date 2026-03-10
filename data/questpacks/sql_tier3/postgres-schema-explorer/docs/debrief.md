## What You Practiced
You successfully navigated an unfamiliar **PostgreSQL** schema using the **Database Explorer** and performed a multi-table lookup.

## Why This Works
By first inspecting the metadata, you avoided "syntax errors" caused by incorrect column names. Using a subquery allowed you to filter by a human-readable name while respecting the database's normalized structure.

## Common Pitfall
Forgetting to account for case sensitivity in string filters. In **PostgreSQL**, `'Engineering'` is not the same as `'engineering'`.

## Job-Style Takeaway
Database exploration is 50% of the job. Before writing a line of code, senior engineers spend time understanding the "Metal" of the database.

## Next Skill
Next, you'll learn to handle **Table Relationships** and many-to-many joins in the Deep Archives.
