SELECT
    event_type,
    payload->>'user_id' AS user_id,
    payload->>'action'  AS action
FROM webhook_events
WHERE payload->>'status' = 'active';
