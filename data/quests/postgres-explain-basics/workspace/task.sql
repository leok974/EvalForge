-- Quest: postgres-explain-basics
-- Goal: Use EXPLAIN to inspect the query plan PostgreSQL chooses for a
--       filtered query on the audit_logs table.

-- TODO: Add the EXPLAIN keyword before the SELECT below
SELECT * FROM audit_logs WHERE user_id = 42 AND action = 'login';
