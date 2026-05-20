INSERT INTO users (id, name, email, age, city, is_active) VALUES (7, 'Grace', 'grace@example.com', 30, 'London', 1);
UPDATE users SET is_active = 0 WHERE city = 'Austin';
DELETE FROM orders WHERE status = 'cancelled';
SELECT id, name, city FROM users ORDER BY id ASC;
