-- example.sql (reference)
-- This demonstrates a JOIN between order_items and products.
-- It is NOT the quest answer.

SELECT
  order_items.order_id,
  products.name AS product_name,
  order_items.qty
FROM order_items
JOIN products ON order_items.product_id = products.id;
