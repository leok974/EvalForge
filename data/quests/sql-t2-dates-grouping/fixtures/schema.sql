DROP TABLE IF EXISTS user_logins;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  manager_id INTEGER,
  salary INTEGER,
  bonus INTEGER,
  hire_date TEXT,
  FOREIGN KEY (manager_id) REFERENCES employees(id)
);

CREATE TABLE events (
  id INTEGER PRIMARY KEY,
  event_type TEXT NOT NULL,
  event_date TEXT NOT NULL
);

CREATE TABLE user_logins (
  user_id INTEGER PRIMARY KEY,
  login_count INTEGER NOT NULL,
  last_login TEXT NOT NULL
);
