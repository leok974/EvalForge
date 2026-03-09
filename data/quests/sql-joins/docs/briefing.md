# Briefing: Relational Mastery

In a relational database, data is spread across multiple [tables](glossary/sql/table). To get a complete picture, you must learn to join them back together.

## Mission

Retrieve a list of orders paired with the name of the user who placed them.

## Requirements

1.  **Join**: Use [JOIN](glossary/sql/join) to connect the `orders` table to the `users` table.
2.  **Condition**: Use the [ON](glossary/sql/on) clause to match `orders.user_id` with `users.id`.
3.  **Columns**: [SELECT](glossary/sql/select) the `orders.id` (aliased as `order_id`) and `users.name` (aliased as `user_name`).

## Success Criteria

-   Every order is paired with a user name.
-   The columns are named `order_id` and `user_name`.
