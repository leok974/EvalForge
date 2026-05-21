SELECT
    DATE_TRUNC('hour', recorded_at) AS hour_bucket,
    COUNT(*)                        AS reading_count
FROM sensor_readings
WHERE recorded_at >= '2024-01-15'
  AND recorded_at <  '2024-01-16'
GROUP BY hour_bucket
ORDER BY hour_bucket;
