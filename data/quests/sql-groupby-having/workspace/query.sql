-- TODO: group errors and filter with HAVING
SELECT service, COUNT(*) AS error_count
FROM events
WHERE status = 'error'
GROUP BY service
HAVING COUNT(*) >= 999
ORDER BY error_count DESC, service ASC;
