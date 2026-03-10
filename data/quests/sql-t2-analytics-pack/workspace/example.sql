-- Example: Simple Lead/Lag analysis
-- This query shows the current month and the NEXT month's revenue
SELECT 
    month,
    revenue,
    LEAD(revenue) OVER (ORDER BY month) as next_month_revenue
FROM monthly_sales;
