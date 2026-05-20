SELECT orders.id AS order_id, users.name AS user_name, orders.total_cents
FROM orders
JOIN users ON orders.user_id = users.id
WHERE orders.status = 'paid'
ORDER BY orders.id ASC;
