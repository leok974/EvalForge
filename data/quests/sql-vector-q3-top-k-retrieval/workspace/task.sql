-- Top-2 Political Search
-- Find the 2 fragments closest to [0.1, 0.1, 0.9]
-- Order by Cosine distance (<=>) and limit the result.

SELECT 
    fragment_id,
    content
FROM 
    historical_fragments
ORDER BY 
    -- Calculate distance to [0.1, 0.1, 0.9]
     <=>  -- Operator and Vector literal here
LIMIT ; -- Limit the result count
