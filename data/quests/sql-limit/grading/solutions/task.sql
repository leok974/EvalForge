SELECT id, name, category, price_cents
FROM products
WHERE is_discontinued = 0
ORDER BY price_cents DESC, name ASC
LIMIT 3;
