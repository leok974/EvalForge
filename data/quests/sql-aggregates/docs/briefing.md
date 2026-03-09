# Briefing: Inventory Summary

The High Archivist requires a summary of the current product inventory to allocate resources correctly.

## Mission

Retrieve a single row summarizing the entire `products` table.

## Requirements

1.  **Count**: Use [COUNT](glossary/sql/count) to find the total number of [rows](glossary/sql/row) in the `products` [table](glossary/sql/table). Name this column `total_count`.
2.  **Sum**: Use [SUM](glossary/sql/sum) to calculate the total `price_cents` of all products. Name this column `total_value_cents`.

## Success Criteria

-   A single row is returned.
-   The columns are named `total_count` and `total_value_cents`.
