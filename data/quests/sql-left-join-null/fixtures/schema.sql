CREATE TABLE departments (
  id   INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE employees (
  id      INTEGER PRIMARY KEY,
  name    TEXT NOT NULL,
  dept_id INTEGER NOT NULL,
  FOREIGN KEY(dept_id) REFERENCES departments(id)
);
