-- sql-t2-boss-data-quality-audit
-- TASK:
-- Audit the database for orphaned manager references.
--
-- Output columns (exact order):
--   id, name, manager_id
--
-- Rules:
-- - First, INSERT a record that violates logic: id=99, name='Ghost Employee', manager_id=999
-- - Then, find all employees whose manager_id does not exist in the employees(id) column.
-- - Use a LEFT JOIN (anti-join) where the right side is NULL
-- - Sort by id ASC
--
-- TODO:
-- Insert the ghost record and then write the anti-join query to audit the table.

-- 1. Insert the record
INSERT INTO employees (id, name, manager_id) VALUES (99, 'Ghost Employee', 999);

-- 2. Audit the table
SELECT 
    e.id, 
    e.name, 
    e.manager_id
FROM employees e
-- TODO: Add LEFT JOIN to find missing managers
ORDER BY e.id ASC;
