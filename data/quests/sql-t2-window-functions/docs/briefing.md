**Quest: Window Functions (T2)**

### The Mission
We need to understand how salaries compare within each department. Instead of a simple average, we want to see where each specific employee ranks against their peers.

Generate a report that assigns a [rank](glossary/sql/window-function) to each employee based on their salary, grouped by their department.

### Requirements
1. **Columns**: Select `name`, `department`, and `salary`.
2. **Mechanism**: Create a new column aliased as `rank`.
3. **Calculation**: Use the `RANK()` function with an [OVER](glossary/sql/over) clause.
4. **Window Logic**:
   - Use [PARTITION BY](glossary/sql/partition-by) `department` to group the ranking.
   - Use `ORDER BY salary DESC` within the window to rank from highest salary to lowest.
