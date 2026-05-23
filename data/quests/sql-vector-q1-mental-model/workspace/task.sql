-- Retrieve the Celestial Record
-- Use the Database Explorer to verify the column names.
-- Find the fragment where fragment_id is 1.

SELECT 
    fragment_id,
    content,
    -- Get the vector data
    embedding
FROM 
    historical_fragments
WHERE 
    fragment_id = ; -- Complete the filter
