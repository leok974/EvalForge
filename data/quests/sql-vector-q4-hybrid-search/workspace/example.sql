-- Example: Earth Filter
-- Finding Agriculture fragments similar to [0.1, 0.8, 0.1]
-- This ensures we don't accidentally get an Astronomy fragment that is 'somewhat' close.

SELECT 
    fragment_id,
    content
FROM 
    historical_fragments
WHERE 
    category = 'Agriculture'
ORDER BY 
    embedding <=> '[0.1, 0.8, 0.1]'::vector
LIMIT 1;
