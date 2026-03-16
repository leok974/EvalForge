INSERT INTO webhook_events (event_type, payload) VALUES
('payment_success', '{"amount": 50.00, "user_id": 101, "metadata": {"priority": "low", "region": "US"}}'),
('payment_success', '{"amount": 500.00, "user_id": 102, "metadata": {"priority": "high", "region": "EU"}}'),
('user_signup', '{"user_id": 103, "source": "referral"}'),
('payment_success', '{"amount": 1200.00, "user_id": 104, "metadata": {"priority": "high", "region": "AS"}}'),
('payment_failed', '{"error_code": "E001", "user_id": 105}');
