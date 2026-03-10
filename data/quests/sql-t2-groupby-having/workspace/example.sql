-- Example: Analyzing Inventory Value
-- This query finds categories with a high average item price.
-- It demonstrates how HAVING works on post-group calculations.

SELECT 
    category, 
    AVG(price) as avg_unit_price
FROM products
GROUP BY category
HAVING AVG(price) > 5.0;
