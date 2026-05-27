-- The Archive Ruler
-- Calculate the Cosine distance to the target vector [0.5, 0.5, 0.5]
-- Use the <=> operator for Cosine distance.

SELECT 
    fragment_id,
    -- Add the distance calculation here
    -- Target: '[0.5, 0.5, 0.5]'::vector
    embedding <=>  as distance
FROM 
    historical_fragments;
