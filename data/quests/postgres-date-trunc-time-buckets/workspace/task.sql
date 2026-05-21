-- Quest: postgres-date-trunc-time-buckets
-- Goal: Group sensor readings into hourly buckets using DATE_TRUNC.
--       Count how many readings occurred each hour on 2024-01-15.

SELECT
    DATE_TRUNC('hour', recorded_at) AS hour_bucket,
    COUNT(*)                        AS reading_count
FROM sensor_readings
-- TODO: filter for a single day: recorded_at >= '2024-01-15' AND recorded_at < '2024-01-16'
-- TODO: GROUP BY hour_bucket
-- TODO: ORDER BY hour_bucket
;
