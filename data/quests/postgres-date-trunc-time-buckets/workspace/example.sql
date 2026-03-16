-- Example: Daily aggregation
-- Useful for seeing long-term trends.

SELECT 
    date_trunc('day', recorded_at) AS day,
    count(*) AS reading_count
FROM sensor_readings
GROUP BY 1
ORDER BY 1 DESC;
