**BOSS Quest: Analytics Pack (T2)**

### The Mission
The board of directors needs a growth report. They don't just want to see raw revenue; they want to see how much we **grew** compared to the previous month.

Use a [CTE](glossary/sql/cte-with) and a [Window Function](glossary/sql/window-function) to build a monthly growth tracker.

### Requirements
1. **CTE**: Define a CTE named `LaggedSales` that calculates:
   - `month`
   - `revenue`
   - `prev_revenue` (using the `LAG()` function over `month`).
2. **Main Query**: Pull from `LaggedSales` and calculate `growth` (`revenue - prev_revenue`).
3. **Filtering**: Exclude the very first month (where `prev_revenue` is [NULL](glossary/sql/null)).
4. **Sort**: Order the final results by `month` in [ascending](glossary/sql/asc) order.
