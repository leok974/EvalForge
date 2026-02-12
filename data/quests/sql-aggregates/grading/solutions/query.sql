SELECT
  COUNT(*) AS count_orders,
  SUM(amount) AS total_amount,
  ROUND(AVG(amount), 2) AS avg_amount
FROM orders;
