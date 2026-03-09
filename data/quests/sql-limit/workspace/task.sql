-- Mission:
-- Show the 3 most expensive active products.
--
-- Requirements:
-- 1) Return: id, name, category, price_cents
-- 2) Only include products that are not discontinued
-- 3) Sort by price_cents descending, then name ascending
-- 4) Return only 3 rows

SELECT
  id,
  name,
  category,
  price_cents
FROM products
WHERE is_discontinued = FALSE
ORDER BY price_cents DESC, name ASC;
