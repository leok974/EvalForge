SELECT category, AVG(price_cents) AS average_price
FROM products
GROUP BY category
HAVING average_price > 1000
ORDER BY average_price DESC;
