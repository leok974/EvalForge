SELECT service, COUNT(*) AS error_count
FROM events
WHERE status = 'error'
GROUP BY service
HAVING COUNT(*) >= 2
ORDER BY error_count DESC, service ASC;
