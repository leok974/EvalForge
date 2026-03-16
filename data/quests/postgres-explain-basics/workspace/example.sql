-- Example: Analyzing a subquery plan
-- Complex queries often benefit from EXPLAIN to see if joins are optimal.

EXPLAIN 
SELECT * FROM audit_logs
WHERE user_id IN (SELECT id FROM audit_logs LIMIT 5);
