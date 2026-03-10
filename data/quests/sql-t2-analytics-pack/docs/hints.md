# Hints: BOSS - Analytics Pack

## Hint 1 — Looking Back
To get a value from the previous row, use the `LAG()` window function.
`LAG(revenue) OVER (ORDER BY month) AS prev_revenue`

## Hint 2 — Calculating Growth
Once you have `prev_revenue` in your CTE, you can simply subtract it from the current revenue in your main query.
`(revenue - prev_revenue) AS growth`

## Hint 3 — Filtering the Start
The first row's `prev_revenue` will be `NULL`. Use a `WHERE` clause to hide it.
`WHERE prev_revenue IS NOT NULL`

## Hint 4 — The Full Solution
```sql
WITH LaggedSales AS (
    SELECT 
        month, 
        revenue,
        LAG(revenue) OVER (ORDER BY month) as prev_revenue
    FROM monthly_sales
)
SELECT 
    month,
    revenue,
    prev_revenue,
    (revenue - prev_revenue) as growth
FROM LaggedSales
WHERE prev_revenue IS NOT NULL;
```
