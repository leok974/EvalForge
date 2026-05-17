DROP TABLE IF EXISTS products;

CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  price_cents INTEGER NOT NULL,
  is_discontinued INTEGER NOT NULL CHECK (is_discontinued IN (0,1))
);
