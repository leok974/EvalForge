INSERT INTO users (id, name, email, age, city, is_active) VALUES
  (1, 'Alice',   'alice@example.com',   28, 'Detroit', 1),
  (2, 'Bob',     'bob@example.com',     35, 'Austin',  1),
  (3, 'Charlie', 'charlie@example.com', 22, 'Detroit', 0),
  (4, 'Diana',   'diana@example.com',   41, 'Seattle', 1),
  (5, 'Evan',    'evan@example.com',    29, 'Austin',  0),
  (6, 'Fay',     'fay@example.com',     33, 'Miami',   1);

INSERT INTO products (id, name, category, price_cents, is_discontinued) VALUES
  (1, 'Laptop',      'electronics', 99900, 0),
  (2, 'Mouse',       'electronics',  2500, 0),
  (3, 'Coffee',      'grocery',       1200, 0),
  (4, 'Headphones',  'electronics',  7500, 1),
  (5, 'Notebook',    'office',         500, 0);

INSERT INTO orders (id, user_id, status, created_at, total_cents) VALUES
  (1, 1, 'paid',      '2025-01-02', 102400),
  (2, 1, 'shipped',   '2025-01-05',   3700),
  (3, 2, 'paid',      '2025-02-10',   9900),
  (4, 3, 'cancelled', '2025-02-11',      0),
  (5, 4, 'paid',      '2025-03-15',   1700),
  (6, 5, 'pending',   '2025-03-20',   7500);

INSERT INTO order_items (order_id, product_id, qty) VALUES
  (1, 1, 1),
  (1, 2, 1),
  (2, 2, 1),
  (2, 3, 1),
  (3, 4, 1),
  (3, 2, 1),
  (5, 5, 2),
  (5, 3, 1),
  (6, 4, 1);
