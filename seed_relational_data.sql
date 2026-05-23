-- 1. Clean and Recreate Structure
DROP TABLE IF EXISTS employee_assignments CASCADE;
DROP TABLE IF EXISTS milestones CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
DROP TABLE IF EXISTS sensor_readings CASCADE;
DROP TABLE IF EXISTS audit_logs CASCADE;
DROP TABLE IF EXISTS webhook_events CASCADE;

CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT
);

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    salary INTEGER,
    secret_key TEXT
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    budget NUMERIC(12, 2)
);

CREATE TABLE employee_assignments (
    employee_id INTEGER REFERENCES employees(id),
    project_id INTEGER REFERENCES projects(id),
    role TEXT,
    PRIMARY KEY (employee_id, project_id)
);

CREATE TABLE milestones (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    name TEXT,
    due_date DATE
);

CREATE TABLE sensor_readings (
    id SERIAL PRIMARY KEY,
    sensor_id TEXT NOT NULL,
    temperature NUMERIC(5, 2),
    recorded_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    event_type TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE webhook_events (
    id SERIAL PRIMARY KEY,
    event_type TEXT NOT NULL,
    payload JSONB NOT NULL
);

-- 2. Populate Data
-- Departments
INSERT INTO departments (id, name, location) VALUES
(1, 'Engineering', 'San Francisco'),
(2, 'Design', 'New York'),
(3, 'Marketing', 'London');

-- Employees
INSERT INTO employees (name, email, department_id) VALUES
('Alice Rivera', 'alice@evalforge.com', 1),
('Bob Chen', 'bob@evalforge.com', 1),
('Charlie Davis', 'charlie@evalforge.com', 2),
('Diana Prince', 'diana@evalforge.com', 3);

INSERT INTO employees (name, email, salary, secret_key) VALUES
('User 1', 'user1@evalforge.com', 50000, 'X-123'),
('User 2', 'user2@evalforge.com', 60000, 'Y-456'),
('User 3', 'user3@evalforge.com', 70000, 'Z-789'),
('User 4', 'user4@evalforge.com', 80000, 'A-012'),
('User 5', 'user5@evalforge.com', 90000, 'B-345'),
('User 6', 'user6@evalforge.com', 100000, 'C-678'),
('User 7', 'user7@evalforge.com', 110000, 'D-901'),
('User 8', 'user8@evalforge.com', 120000, 'E-234'),
('User 9', 'user9@evalforge.com', 130000, 'F-567'),
('User 10', 'user10@evalforge.com', 140000, 'G-890');

-- Projects
INSERT INTO projects (id, name, budget) VALUES
(1, 'Project Phoenix', 120000.00),
(2, 'Project Icarus', 45000.00),
(3, 'Project Chronos', 85000.00);

-- Assignments
INSERT INTO employee_assignments (employee_id, project_id, role)
SELECT e.id, p.id, t.role
FROM (VALUES 
    ('Alice Rivera', 'Project Phoenix', 'Lead Engineer'),
    ('Bob Chen', 'Project Phoenix', 'QA'),
    ('Charlie Davis', 'Project Phoenix', 'UI Designer'),
    ('Alice Rivera', 'Project Icarus', 'Consultant'),
    ('Bob Chen', 'Project Chronos', 'DevOps'),
    ('Diana Prince', 'Project Chronos', 'Campaign Manager')
) AS t(emp_name, proj_name, role)
JOIN employees e ON e.name = t.emp_name
JOIN projects p ON p.name = t.proj_name;

-- Milestones
INSERT INTO milestones (project_id, name, due_date) VALUES
(1, 'Alpha Release', '2024-06-01'),
(1, 'Beta Release', '2024-09-01'),
(3, 'Market Launch', '2024-12-01');

-- Sensor Readings
INSERT INTO sensor_readings (sensor_id, temperature, recorded_at) VALUES
('S-01', 22.5, '2024-10-01 10:05:00+00'),
('S-01', 22.7, '2024-10-01 10:45:00+00'),
('S-01', 23.1, '2024-10-01 11:15:00+00'),
('S-01', 23.5, '2024-10-01 11:55:00+00'),
('S-01', 24.2, '2024-10-01 12:10:00+00'),
('S-01', 24.5, '2024-10-01 13:05:00+00'),
('S-01', 24.4, '2024-10-01 13:50:00+00'),
('S-01', 21.0, '2024-10-02 10:00:00+00');

-- Audit Logs
INSERT INTO audit_logs (event_type, user_id, created_at)
SELECT 
    CASE WHEN (random() > 0.5) THEN 'login' ELSE 'logout' END,
    (random()*1000)::int,
    timestamp '2024-01-01 00:00:00' + random() * (interval '30 days')
FROM generate_series(1, 2000);

-- Webhook Events
INSERT INTO webhook_events (event_type, payload) VALUES
('payment_success', '{"amount": 50.00, "user_id": 101, "metadata": {"priority": "low", "region": "US"}}'),
('payment_success', '{"amount": 500.00, "user_id": 102, "metadata": {"priority": "high", "region": "EU"}}'),
('user_signup', '{"user_id": 103, "source": "referral"}'),
('payment_success', '{"amount": 1200.00, "user_id": 104, "metadata": {"priority": "high", "region": "AS"}}'),
('payment_failed', '{"error_code": "E001", "user_id": 105}');
