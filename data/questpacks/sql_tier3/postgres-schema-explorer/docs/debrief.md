## What You Practiced
You successfully performed **Schema Exploration** on an unfamiliar **PostgreSQL** database and implemented a filtered result set using normalized table relationships.

## Why This Works
By first inspecting the metadata, you avoided "hidden" errors caused by incorrect column names. Using a subquery allowed you to filter by the human-readable string `'Engineering'` while maintaining optimal database performance.

## Common Pitfall
**Case Sensitivity**. In **PostgreSQL**, string comparisons are case-sensitive by default. Searching for `'engineering'` instead of `'Engineering'` would return zero results in this schema.

## Job-Style Takeaway
Database exploration is 50% of the job. Senior engineers spend more time understanding the **"Metal"** of the schema than they do writing the final `SELECT` statement.

## Next Skill
Next, you'll tackle **Table Relationships** and complex many-to-many joins in the Deep Archives.
