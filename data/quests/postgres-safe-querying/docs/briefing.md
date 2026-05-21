# PostgreSQL: Safe Querying

You have been given access to a production database. Before running any expensive queries, a responsible engineer does two things: inspect the schema to understand available columns, then preview data with a row limit before touching anything at scale.

Your task: use `information_schema.columns` to list the column metadata for the `employees` table (column name, data type, and whether it is nullable), ordered by column position, and limit the result to 5 rows.
