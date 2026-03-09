# Mission: Filter the Data

**World:** SQL Fundamentals — **Quest:** [WHERE](glossary/sql/where) Clause

---

## Situation

The "Oracle of Detroit" has requested a list of users who are currently **active** and reside in **Detroit**. 

Your goal is to produce a refined list of users that the High Scribes can use to contact the local resistance.

## Requirements

1.  **Columns**: [SELECT](glossary/sql/select) the `name`, `age`, and `city` of the users.
2.  **Filter**: Use a [WHERE](glossary/sql/where) clause to restrict the results to:
    -   `city` must be exactly `'Detroit'`.
    -   `is_active` must be `1` (True).
3.  **Sort**: [ORDER BY](glossary/sql/order-by) the user's `name` in [ascending](glossary/sql/asc) order.

## Success Criteria

-   Only rows matching both conditions are returned.
-   Columns appear in the order: `name`, `age`, `city`.
-   The list is alphabetized by `name`.
