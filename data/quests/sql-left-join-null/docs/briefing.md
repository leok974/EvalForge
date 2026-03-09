# Briefing: The Empty Spaces

Not all connections are complete. Sometimes, the most important data is the data that *isn't* there.

## Mission

Identify every user in our system who has never placed an order.

## Requirements

1.  **Left Join**: Use [LEFT JOIN](glossary/sql/join) to combine `users` with `orders`. Unlike an INNER JOIN, a LEFT JOIN will keep all users even if they don't have a matching order.
2.  **Condition**: Join on `users.id = orders.user_id`.
3.  **Filter**: Use a [WHERE](glossary/sql/where) clause with **[IS NULL](glossary/sql/null)** to find the users who have no match in the `orders` table.
4.  **Columns**: [SELECT](glossary/sql/select) only the `users.name` (aliased as `user_name`).

## Success Criteria

-   Only users with zero orders are returned.
-   The column is named `user_name`.
