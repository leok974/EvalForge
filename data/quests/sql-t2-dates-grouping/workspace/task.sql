-- sql-t2-dates-grouping
-- TASK:
-- Count the total number of events for each day.
--
-- Output columns (exact order):
--   event_date_only, num_events
--
-- Rules:
-- - event_date_only: result of strftime('%Y-%m-%d', event_date)
-- - num_events: count of rows
-- - Sort by event_date_only ASC
--
-- TODO:
-- Update the query below to bucket the timestamps into dates and count them.

SELECT
  event_date -- TODO: Transform this to 'YYYY-MM-DD' format
FROM events;
