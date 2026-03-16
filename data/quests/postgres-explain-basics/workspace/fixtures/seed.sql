-- Seeding enough data to make performance visible
INSERT INTO audit_logs (event_type, user_id, created_at)
SELECT 
    CASE WHEN (random() > 0.5) THEN 'login' ELSE 'logout' END,
    (random()*1000)::int,
    timestamp '2024-01-01 00:00:00' + random() * (interval '30 days')
FROM generate_series(1, 2000);
