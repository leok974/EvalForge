**Quest: NULL Semantics & COALESCE**

### The Mission
The payroll department is reporting a bug in their reports: employees with no documented bonus are showing up with a total compensation of "NULL" instead of their base salary.

Your goal is to fix the calculation using a [coalesce](glossary/sql/coalesce) strategy.

### Requirements
1. **Columns**: Select `id`, `name`, and calculate `total_comp` (salary + bonus).
2. **Handle NULLs**: Use `COALESCE(bonus, 0)` to ensure the calculation works even when bonus is [NULL](glossary/sql/null).
3. **Sort**: Order the results by `total_comp` in [descending](glossary/sql/desc) order, then by `id` in [ascending](glossary/sql/asc) order to break ties.
