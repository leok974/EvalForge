-- example.sql (reference)
-- This demonstrates a LEFT JOIN between products and order_items.
-- It shows all products, even those that haven't been ordered (where order_id will be NULL).
-- It is NOT the quest answer.

SELECT
  products.name AS product_name,
  order_items.order_id
FROM products
LEFT JOIN order_items ON products.id = order_items.product_id;
