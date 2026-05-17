-- Note: within Austin, Evan is inserted before Bob intentionally.
-- This ensures ORDER BY city ASC alone (no secondary key) fails the test.
INSERT INTO users (id, name, email, age, city, is_active) VALUES
  (1, 'Alice',   'alice@example.com',   28, 'Detroit', 1),
  (2, 'Evan',    'evan@example.com',    29, 'Austin',  0),
  (3, 'Charlie', 'charlie@example.com', 22, 'Detroit', 0),
  (4, 'Diana',   'diana@example.com',   41, 'Seattle', 1),
  (5, 'Bob',     'bob@example.com',     35, 'Austin',  1),
  (6, 'Fay',     'fay@example.com',     33, 'Miami',   1);
