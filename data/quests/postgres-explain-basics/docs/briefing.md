# PostgreSQL: EXPLAIN Basics

Your application has a slow query against the `audit_logs` table that filters by `user_id` and `action`. Before adding an index or rewriting the query, you need to see the query plan PostgreSQL chose — is it doing a sequential scan or using an index?

Your task: prefix the SELECT statement with `EXPLAIN` to print the query plan without executing the query. Read the plan output to understand how PostgreSQL will access the data.
