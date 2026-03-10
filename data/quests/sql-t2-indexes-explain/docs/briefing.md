**Quest: Indexes & EXPLAIN**

### The Mission
The Archive's retrieval systems are slowing down. Queries to find which employees report to a specific manager are taking too long.

Optimize the system by creating a [performance-enhancing index](glossary/sql/index) and verify that the database uses it.

### Requirements
1. **Creation**: Create an [index](glossary/sql/index) named `idx_emp_mgr` on the `manager_id` column of the `employees` table.
2. **Analysis**: Use the [EXPLAIN QUERY PLAN](glossary/sql/explain-query-plan) command on a query that selects all columns from `employees` where `manager_id = 1`.
3. **Validation**: The objective system will check the output of your `EXPLAIN` statement to ensure it says `SEARCH` instead of `SCAN`.
