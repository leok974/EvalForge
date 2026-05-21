SELECT city, COUNT(*) AS user_count
FROM users
GROUP BY city
HAVING user_count >= 2
ORDER BY city ASC;
