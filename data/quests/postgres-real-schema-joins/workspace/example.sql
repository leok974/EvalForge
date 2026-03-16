-- Example: Joining projects and milestones
-- This shows how to link projects to their upcoming deadlines.

SELECT 
    p.name AS project_name,
    m.name AS milestone_name,
    m.due_date
FROM projects AS p
JOIN milestones AS m ON p.id = m.project_id
ORDER BY m.due_date;
