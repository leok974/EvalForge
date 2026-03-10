-- sql-t2-recursive-cte-hierarchy
-- TASK:
-- Build an organizational hierarchy chart.
--
-- Output columns (exact order):
--   id, name, distance
--
-- Rules:
-- - Use WITH RECURSIVE OrgChart
-- - Anchor: employees with manager_id IS NULL (distance 0)
-- - Recursion: employees joining to OrgChart on manager_id (distance + 1)
-- - Sort by distance ASC, id ASC
--
-- TODO:
-- Complete the RECURSIVE member and the final SELECT.

WITH RECURSIVE OrgChart AS (
    -- Anchor member
    SELECT id, name, manager_id, 0 as distance
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive member
    SELECT 
        e.id, 
        e.name, 
        e.manager_id, 
        o.distance + 1
    FROM employees e
    -- TODO: Add JOIN to OrgChart here
)
-- TODO: Add final SELECT
;
