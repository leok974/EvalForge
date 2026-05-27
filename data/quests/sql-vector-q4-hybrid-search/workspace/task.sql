-- The Celestial Specialist
-- Filter by category 'Astronomy'
-- Rank by Cosine distance to [0.9, 0.1, 0.1]

SELECT 
    fragment_id,
    content
FROM 
    historical_fragments
WHERE 
    category =  -- Filter here
ORDER BY 
    embedding <=>  -- Rank here
LIMIT ;
