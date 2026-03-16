-- Example: Metric Comparison
-- Find the distance to [1, 0, 0] (Pure Astronomy) using two different rulers.
-- Result: You will see that 'Astronomy' records have much smaller distances.

SELECT 
    fragment_id,
    content,
    embedding <-> '[1, 0, 0]'::vector as l2_dist,
    embedding <=> '[1, 0, 0]'::vector as cosine_dist
FROM 
    historical_fragments
ORDER BY 
    cosine_dist;
