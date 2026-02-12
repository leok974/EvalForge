INSERT INTO tasks (id, title, status) VALUES (4, 'monitor', 'todo');

UPDATE tasks
SET status = 'done'
WHERE id = 2;

DELETE FROM tasks
WHERE id = 3;

SELECT id, title, status
FROM tasks
ORDER BY id ASC;
