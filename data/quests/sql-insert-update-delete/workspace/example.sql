-- example.sql (reference)
-- This demonstrates inserting new data.
-- It is NOT the quest answer.

INSERT INTO products (id, name, category, price_cents, is_discontinued)
VALUES (6, 'Keyboard', 'electronics', 4500, 0);

SELECT * FROM products;
