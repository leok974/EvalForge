# PostgreSQL: Date Trunc & Time Buckets

A sensor network logged temperature readings every few minutes on 2024-01-15. Your team needs to understand hourly patterns: how many readings were taken each hour that day?

Your task: use `DATE_TRUNC('hour', recorded_at)` to group readings into hourly buckets, count the readings per bucket, and filter for the target day only. Return results ordered chronologically.
