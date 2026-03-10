-- sql-t2-cte-basics
-- TASK:
-- Use a CTE to filter high-volume event types.
--
-- Output columns (exact order):
--   event_type, num_events
--
-- Rules:
-- - Use a CTE named 'EventCounts'
-- - CTE should select event_type and COUNT(*) as num_events
-- - Main query selects from the CTE where num_events > 1
-- - Sort by event_type ASC
--
-- TODO:
-- Wrap the query below in a WITH clause and add the final filter.

SELECT 
    event_type, 
    COUNT(*) as num_events 
FROM events 
GROUP BY event_type;
