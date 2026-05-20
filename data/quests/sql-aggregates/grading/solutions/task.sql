SELECT COUNT(*) AS total_count, SUM(total_cents) AS total_value_cents FROM orders WHERE status = 'paid';
