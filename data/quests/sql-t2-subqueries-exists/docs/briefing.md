**Quest: Correlated Subqueries & EXISTS**

### The Mission
The organization is growing, and we need to verify which employees have taken on management responsibilities.

Identify all employees who are **managers** by checking if their `id` appears as a `manager_id` for any other employee.

### Requirements
1. **Columns**: Select `id` and `name` from the `employees` [table](glossary/sql/table).
2. **Mechanism**: Use the [EXISTS](glossary/sql/exists) operator with a correlated [subquery](glossary/sql/subquery).
3. **Condition**: The subquery should check the `employees` table for any row where `manager_id` matches the `id` of the current employee in the outer query.
4. **Sort**: Order by `id` in [ascending](glossary/sql/asc) order.
