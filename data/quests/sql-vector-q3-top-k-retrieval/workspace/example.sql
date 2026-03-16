SELECT 
    fragment_id,
    content,
    embedding <=> '[0, 1, 0]'::vector as distance
FROM historical_fragments
ORDER BY 3
LIMIT 3;
