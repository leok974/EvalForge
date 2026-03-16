-- Example: Chaining JSONB extractions
-- Shows how to dig deep into a nested object.

SELECT 
    payload -> 'metadata' ->> 'priority' AS priority,
    count(*)
FROM webhook_events
GROUP BY 1;
