INSERT INTO departments (name, location) VALUES
('Engineering', 'San Francisco'),
('Design', 'New York'),
('Marketing', 'London');

INSERT INTO employees (name, email, department_id) VALUES
('Alice Rivera', 'alice@evalforge.com', 1),
('Bob Chen', 'bob@evalforge.com', 1),
('Charlie Davis', 'charlie@evalforge.com', 2),
('Diana Prince', 'diana@evalforge.com', 3);

INSERT INTO projects (name, budget) VALUES
('Project Phoenix', 120000.00),
('Project Icarus', 45000.00),
('Project Chronos', 85000.00);

INSERT INTO employee_assignments (employee_id, project_id, role) VALUES
(1, 1, 'Lead Engineer'),
(2, 1, 'QA'),
(3, 1, 'UI Designer'),
(1, 2, 'Consultant'),
(2, 3, 'DevOps'),
(4, 3, 'Campaign Manager');

INSERT INTO milestones (project_id, name, due_date) VALUES
(1, 'Alpha Release', '2024-06-01'),
(1, 'Beta Release', '2024-09-01'),
(3, 'Market Launch', '2024-12-01');
