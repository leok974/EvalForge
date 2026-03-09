# Briefing: Composable Queries

As queries grow in complexity, they can become difficult to read. [CTEs](glossary/sql/cte) (Common Table Expressions) allow you to break your query into logical building blocks.

## Mission

Calculate the total spend (the sum of `total_cents` from orders) for every **active** user.

## Requirements

1.  **CTE**: Use the `WITH` clause to create a [CTE](glossary/sql/cte) named `active_users` that selects all users where `is_active = 1`.
2.  **Join**: Join the `active_users` CTE with the `orders` [table](glossary/sql/table).
3.  **Aggregate**: Calculate the [SUM](glossary/sql/sum) of `total_cents` for each user. Name this column `total_spend`.
4.  **Columns**: [SELECT](glossary/sql/select) the `name` (as `user_name`) and `total_spend`.

## Success Criteria

-   Only active users are included in the results.
-   The columns are named `user_name` and `total_spend`.
-   The query uses a `WITH` clause.
