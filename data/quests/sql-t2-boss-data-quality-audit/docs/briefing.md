**BOSS Quest: Data Quality Audit (T2)**

### The Mission
A recent system migration was messy. Rumor has it that some employees have been assigned to managers who don't actually exist in our personnel file. These "orphaned" records are causing bugs in the payroll system.

First, you will intentionally damage the data to test your detection logic, then you will write the audit query to find the broken link.

### Requirements
1. **Creation**: `INSERT` a new employee with `id = 99`, `name = 'Ghost Employee'`, and `manager_id = 999`. (Note: Manager `999` does not exist in the table).
2. **Detection**: Write a query that finds all employees whose `manager_id` is NOT [NULL](glossary/sql/null) but whose corresponding manager record is **missing** from the `employees` table.
3. **Mechanism**: Use a `LEFT JOIN` on the table itself (self-join) and filter for rows where the joined manager `id` is `NULL`.
4. **Columns**: Return `id`, `name`, and `manager_id` for the orphaned employees.
5. **Sort**: Order by `id` [ascending](glossary/sql/asc).
