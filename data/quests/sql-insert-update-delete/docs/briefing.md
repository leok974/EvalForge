# Briefing: The Living Archive

A database is not a static tomb; it is a dynamic record of a changing world. To maintain the Archive, you must master the art of data mutation.

## Mission

Update the state of the world by adding a new user, correcting an existing record, and removing obsolete data.

## Requirements

1.  **Addition**: Use [INSERT](glossary/sql/insert) to add a new user named 'Grace'. Ensure every column from `id` to `is_active` is populated.
2.  **Correction**: Use [UPDATE](glossary/sql/update) to change Bob's (`id = 2`) current `city` to 'London'.
3.  **Removal**: Use [DELETE](glossary/sql/delete) to purge the record for order `id = 4` from the `orders` [table](glossary/sql/table).

## Success Criteria

-   A new user 'Grace' exists in the `users` table.
-   Bob's city is successfully updated to 'London'.
-   Order `id = 4` no longer exists in the `orders` table.
