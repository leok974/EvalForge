# Briefing: Premium Categories

The Archivist needs to identify "Premium Categories" — sectors where the average value of products is exceptionally high.

## Mission

Group our product inventory by category and identify those where the average price exceeds 5000 cents.

## Requirements

1.  **Grouping**: Use [GROUP BY](glossary/sql/group-by) to bucket the `products` by their `category`.
2.  **Aggregation**: Calculate the [average](glossary/sql/avg) `price_cents` for each category. Name this column `average_price`.
3.  **Filtering**: Use [HAVING](glossary/sql/having) to only include categories where the `average_price` is greater than 5000.

## Success Criteria

-   Only categories with a high average price are returned.
-   The columns are named `category` and `average_price`.
