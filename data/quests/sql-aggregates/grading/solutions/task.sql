SELECT COUNT(*) AS total_count, SUM(total_cents) AS total_value_cents, AVG(total_cents) AS avg_value_cents
FROM orders
WHERE status = 'paid';
