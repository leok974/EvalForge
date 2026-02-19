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
