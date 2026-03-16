-- Example: Viewing all Political fragments
-- Notice how their embeddings all have a high 3rd dimension.

SELECT 
    fragment_id, 
    content, 
    embedding 
FROM 
    historical_fragments 
WHERE 
    category = 'Politics';
