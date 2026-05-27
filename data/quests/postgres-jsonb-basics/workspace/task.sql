-- Quest: postgres-jsonb-basics
-- Goal: Extract fields from a JSONB payload column using the ->> operator.
--       Filter rows where a nested JSON key has a specific value.

SELECT
    event_type,
    -- TODO: extract 'user_id' from payload using ->> operator, alias as user_id
    -- TODO: extract 'action'  from payload using ->> operator, alias as action
    payload
FROM webhook_events
-- TODO: filter WHERE payload->>'status' = 'active'
;
