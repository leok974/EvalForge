**Quest: Recursive CTEs (Hierarchy)**

### The Mission
The Archive's registry is organized like a tree, but it's currently stored as a flat list. We need to visualize the complete organizational hierarchy.

Use a [recursive CTE](glossary/sql/cte-recursive) to traverse the `employees` table, starting from the CEO and moving down through every level of management.

### Requirements
1. **CTE**: Create a `WITH RECURSIVE` CTE named `OrgChart`.
2. **Anchor**: Start with the employee(s) who have **no manager** (`manager_id IS NULL`). Set their `distance` to `0`.
3. **Recursion**: Join the `employees` table to the `OrgChart` CTE where `employee.manager_id = OrgChart.id`. Increment the `distance` by `1` for each level.
4. **Final Select**: Return `id`, `name`, and `distance`.
5. **Sort**: Order by `distance` [ascending](glossary/sql/asc), then by `id` [ascending](glossary/sql/asc).
