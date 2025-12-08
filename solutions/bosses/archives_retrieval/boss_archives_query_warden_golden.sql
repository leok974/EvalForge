-- Boss: Archives Query Warden
-- Golden Solution (Reference)
--
-- Schema:
--   users(id, name, role, created_at)
--   books(id, title, category, page_count)
--   loans(id, user_id, book_id, loaned_at, returned_at)
--   fines(id, user_id, amount, issued_at, resolved_at)
--
-- Conventions:
--   - We use u, b, l, f as table aliases.
--   - Each task is labeled with a comment.
--   - Queries are written for a Postgres-like dialect.


/*****************************************************************
 TASK 1
 "Top 5 most borrowed books in the last 90 days.
  Return: title, category, borrow_count, ordered by borrow_count desc."
******************************************************************/

-- TASK 1 – Top 5 most borrowed books in last 90 days
SELECT
  b.title,
  b.category,
  COUNT(*) AS borrow_count
FROM loans AS l
JOIN books AS b
  ON b.id = l.book_id
WHERE
  l.loaned_at >= (CURRENT_DATE - INTERVAL '90 days')
GROUP BY
  b.id, b.title, b.category
ORDER BY
  borrow_count DESC,
  b.title ASC
LIMIT 5;


/*****************************************************************
 TASK 2
 "For each user, count active loans (not returned).
  Only include users with more than 2 active loans.
  Return: user_id, name, active_loans, ordered by active_loans desc."
******************************************************************/

-- TASK 2 – Users with more than 2 active loans
SELECT
  u.id AS user_id,
  u.name,
  COUNT(*) AS active_loans
FROM loans AS l
JOIN users AS u
  ON u.id = l.user_id
WHERE
  l.returned_at IS NULL
GROUP BY
  u.id, u.name
HAVING
  COUNT(*) > 2
ORDER BY
  active_loans DESC,
  u.name ASC;


/*****************************************************************
 TASK 3
 "For each book category, show:
    - total_loans (all time),
    - unique_borrowers,
    - avg_page_count for books in that category.
  Return: category, total_loans, unique_borrowers, avg_page_count."
******************************************************************/

-- TASK 3 – Category-level engagement
SELECT
  b.category,
  COUNT(l.id) AS total_loans,
  COUNT(DISTINCT l.user_id) AS unique_borrowers,
  AVG(b.page_count)::NUMERIC(10,2) AS avg_page_count
FROM books AS b
LEFT JOIN loans AS l
  ON b.id = l.book_id
GROUP BY
  b.category
ORDER BY
  total_loans DESC,
  b.category ASC;


/*****************************************************************
 OPTIONAL TASK 4 (Stretch)
 "Total unpaid fines per user."
******************************************************************/

-- TASK 4 (Optional) – Outstanding fines per user
SELECT
  u.id AS user_id,
  u.name,
  COALESCE(SUM(f.amount), 0) AS outstanding_fines
FROM users AS u
LEFT JOIN fines AS f
  ON f.user_id = u.id
 AND f.resolved_at IS NULL
GROUP BY
  u.id, u.name
HAVING
  COALESCE(SUM(f.amount), 0) > 0
ORDER BY
  outstanding_fines DESC,
  u.name ASC;
