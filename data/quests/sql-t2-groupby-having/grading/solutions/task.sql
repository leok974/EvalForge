SELECT category, COUNT(*) as count
FROM products
GROUP BY category
HAVING COUNT(*) > 5;
