INSERT INTO employees (id, name, manager_id, salary, bonus, hire_date) VALUES
(1, 'Alice (CEO)', NULL, 200000, 50000, '2020-01-01'),
(2, 'Bob (VP)', 1, 150000, NULL, '2020-06-15'),
(3, 'Charlie (Manager)', 2, 100000, 10000, '2021-03-20'),
(4, 'Diana (IC)', 3, 80000, NULL, '2022-08-10'),
(5, 'Evan (IC)', 3, 75000, 5000, '2023-01-05');

INSERT INTO events (id, event_type, event_date) VALUES
(1, 'click', '2023-10-01 10:00:00'),
(2, 'view', '2023-10-01 12:30:00'),
(3, 'click', '2023-10-02 09:15:00'),
(4, 'purchase', '2023-10-02 14:00:00'),
(5, 'view', '2023-10-03 16:45:00'),
(6, 'click', '2023-10-03 16:50:00');

INSERT INTO user_logins (user_id, login_count, last_login) VALUES
(1, 10, '2023-09-01'),
(2, 5, '2023-09-15');
