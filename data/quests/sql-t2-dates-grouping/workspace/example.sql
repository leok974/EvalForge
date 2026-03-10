-- Example: Counting events by hour
-- This query shows activity patterns throughout the day
SELECT 
  strftime('%H', event_date) AS hour,
  COUNT(*) AS activity_count
FROM events
GROUP BY hour;
