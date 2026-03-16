INSERT INTO departments (name, building) VALUES 
('Engineering', 'Apollo'),
('Marketing', 'Vesta'),
('Research', 'Athena');

INSERT INTO employees (name, email, department_id, salary, hired_at, skills) VALUES
('Alice', 'alice@evalforge.com', 1, 120000, '2023-01-15 09:00:00+00', ARRAY['Postgres', 'React']),
('Bob (Admin)', 'bob.admin@Example.com', 1, 115000, '2023-02-20 10:00:00+00', ARRAY['Python', 'K8s']),
('Charlie', 'charlie@evalforge.com', 2, 95000, '2023-03-10 11:00:00+00', ARRAY['SEO', 'Copywriting']),
('Diana', 'diana@evalforge.com', 3, 135000, '2023-04-05 08:00:00+00', ARRAY['ML', 'PyTorch']);

INSERT INTO document_embeddings (content, embedding) VALUES
('Company Handbook', '[0.1, 0.2, 0.3]'),
('Engineering Guide', '[0.5, 0.6, 0.7]');
