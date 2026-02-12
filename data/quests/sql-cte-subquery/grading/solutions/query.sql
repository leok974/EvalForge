WITH dept_avg AS (
  SELECT dept_id, AVG(salary) AS avg_salary
  FROM employees
  GROUP BY dept_id
)
SELECT e.name AS employee, d.name AS department, e.salary AS salary
FROM employees e
JOIN dept_avg a ON a.dept_id = e.dept_id
JOIN departments d ON d.id = e.dept_id
WHERE e.salary > a.avg_salary
ORDER BY e.salary DESC, e.name ASC;
