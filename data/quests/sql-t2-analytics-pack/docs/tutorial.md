# Tutorial: BOSS - Analytics Pack (LAG and CTEs)

Welcome to the first BOSS quest of Tier 2. In this challenge, you will combine two powerful techniques: **Common Table Expressions (CTEs)** and **Window Functions**.

## The LAG() Function

The `LAG()` function allows you to look back at the *previous* row in your result set. This is essential for calculating trends, such as month-over-month growth.

```sql
SELECT 
  month, 
  revenue,
  LAG(revenue) OVER (ORDER BY month) as prev_month_revenue
FROM monthly_sales;
```

## Strategy: The Multi-Step Pipeline

Complex calculations (like growth percentages) are much easier to build in two steps using a [CTE](glossary/sql/cte-with):

1. **Step 1 (The CTE)**: Generate the lagged data. 
2. **Step 2 (The Main Query)**: Perform the final math (e.g., `revenue - prev_revenue`) using the columns from your CTE.

## Dealing with the First Row

The very first row in a lagged query will always have a [NULL](glossary/sql/null) for the "previous" value (since there is nothing before it). You will often need to filter these out using `WHERE prev_revenue IS NOT NULL`.

In this BOSS quest, you will calculate the raw growth in revenue between consecutive months.
