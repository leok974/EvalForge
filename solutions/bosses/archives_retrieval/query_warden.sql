-- Boss: Archives Query Warden
-- Mission: Retrieve a list of 'High Value' Patrons who have borrowed books from both the 'Science' and 'History' wings
-- in the last 90 days, sorted by their total loan count descending.

-- Schema Assumptions for this problem:
-- Table: patrons (id, name, join_date)
-- Table: books (id, title, genre)
-- Table: loans (id, book_id, patron_id, loan_date, return_date)

WITH RecentLoans AS (
    SELECT 
        l.patron_id, 
        b.genre,
        COUNT(*) as loan_count
    FROM loans l
    JOIN books b ON l.book_id = b.id
    WHERE l.loan_date >= DATE('now', '-90 days')
    GROUP BY l.patron_id, b.genre
)

SELECT 
    p.name,
    SUM(rl.loan_count) as total_recent_loans
FROM patrons p
JOIN RecentLoans rl ON p.id = rl.patron_id
WHERE p.id IN (
    -- Patrons who have borrowed Science books
    SELECT patron_id FROM RecentLoans WHERE genre = 'Science'
) 
AND p.id IN (
    -- Patrons who have borrowed History books
    SELECT patron_id FROM RecentLoans WHERE genre = 'History'
)
GROUP BY p.id, p.name
ORDER BY total_recent_loans DESC;
