# Boss: Archive Query Warden – Golden Analytics Query Incident Runbook

Scenario: After a query change, **DAU and revenue by country** are too high for some countries, missing for others, and the report is slower.

---

## Incident Context

- **Tables:**
  - `events(user_id, event_type, event_ts, country_code)`
  - `orders(order_id, user_id, amount, currency, created_at, country_code)`
  - `countries(country_code, region, is_active)`

- **Symptoms:**
  - DAU appears inflated compared to historical levels.
  - Some countries show 0 users/revenue despite known activity.
  - Query execution time has increased significantly.

- **Goal:**
  - Restore correct DAU + revenue by country per day.
  - Improve performance.
  - Leave a reusable runbook.

---

## Phase 1 – Clarify the Metric

1. **Define DAU (Daily Active Users)**

   - Grain: **day + country + user**.
   - A user is counted as active for a (day, country) if they have at least one qualifying event in that day with that `country_code`.
   - Metric: `COUNT(DISTINCT user_id)` per (day, country).

2. **Define Revenue**

   - Grain: **day + country**.
   - Sum of `amount` from `orders` whose `created_at` falls in that day and whose `country_code` matches.

3. **Time Window & Time Zone**

   - Use **UTC days** in this runbook (explicit choice).
   - Day boundary: `[00:00, 24:00)` UTC.
   - Validation: later we can compare with local-time dashboards if needed.

---

## Phase 2 – Inspect Current Query & Data

4. **Capture the current query (before change)**

   - Save the existing SQL to a file `queries/dau_revenue_by_country_current.sql`.

5. **Look for red flags**

   - Unscoped joins between `events` and `orders` on `user_id` only.
   - Aggregation after multi-table joins without controlling grain.
   - Filters that might drop rows (e.g., `WHERE countries.is_active = TRUE` with INNER JOIN).

6. **Sample the data**

   - Spot-check per-user events:

```sql
SELECT user_id,
       MIN(event_ts) AS first_event,
       MAX(event_ts) AS last_event,
       COUNT(*)      AS event_count,
       ARRAY_AGG(DISTINCT country_code) AS countries
FROM events
WHERE event_ts >= TIMESTAMP '2025-01-01'
GROUP BY user_id
LIMIT 50;
```

* Inspect orders:

```sql
SELECT country_code,
       COUNT(*)     AS orders_count,
       SUM(amount)  AS revenue
FROM orders
WHERE created_at >= TIMESTAMP '2025-01-01'
GROUP BY country_code
ORDER BY revenue DESC;
```

---

## Phase 3 – Propose Corrected Query

7. **Compute DAU by day + country (subquery)**

```sql
WITH daily_dau AS (
  SELECT
    DATE_TRUNC('day', event_ts) AS event_date_utc,
    country_code,
    COUNT(DISTINCT user_id) AS dau
  FROM events
  WHERE event_ts >= :start_ts
    AND event_ts < :end_ts
  GROUP BY 1, 2
),
daily_revenue AS (
  SELECT
    DATE_TRUNC('day', created_at) AS order_date_utc,
    country_code,
    SUM(amount) AS revenue
  FROM orders
  WHERE created_at >= :start_ts
    AND created_at < :end_ts
  GROUP BY 1, 2
)
SELECT
  d.event_date_utc AS date_utc,
  c.country_code,
  c.region,
  COALESCE(d.dau, 0)      AS dau,
  COALESCE(r.revenue, 0)  AS revenue
FROM countries c
LEFT JOIN daily_dau d
  ON c.country_code = d.country_code
LEFT JOIN daily_revenue r
  ON c.country_code = r.country_code
 AND d.event_date_utc = r.order_date_utc
WHERE c.is_active = TRUE
  AND d.event_date_utc IS NOT NULL
ORDER BY date_utc, c.country_code;
```

* Key points:

  * Compute DAU and revenue in **separate aggregates**, then join at the appropriate grain.
  * Use `LEFT JOIN` from `countries` to keep countries visible even with 0 activity.
  * Use `DISTINCT user_id` to avoid double-counts.

---

## Phase 4 – Performance & Safety Checks

8. **Check the query plan (EXPLAIN)**

```sql
EXPLAIN ANALYZE
WITH daily_dau AS ( ... ), daily_revenue AS ( ... )
SELECT ...
```

* Ensure:

  * Filters on `event_ts` and `created_at` are pushed into scans.
  * Indexes (or partitions) exist on:

    * `events(event_ts, country_code, user_id)`
    * `orders(created_at, country_code, user_id)`

9. **Add/adjust indexes if needed** (warehouse-specific):

```sql
-- Example for Postgres:
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_date_country_user
  ON events (DATE_TRUNC('day', event_ts), country_code, user_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_date_country
  ON orders (DATE_TRUNC('day', created_at), country_code);
```

(Or equivalent partitioning/clustered index strategy in your warehouse.)

10. **Limit scope during testing**

* Start with a narrower date range (e.g., last 7 days) to test performance and correctness.
* Use `LIMIT` + `ORDER BY` where appropriate for spot checks (but remove before production).

---

## Phase 5 – Validation & Rollout

11. **Correctness checks**

* Compare old vs new query for **a few specific cases**:

```sql
-- Per-user spot check
SELECT event_date_utc, country_code, COUNT(DISTINCT user_id) AS dau
FROM (
  -- new query or its subquery
) t
WHERE country_code = 'US'
  AND event_date_utc BETWEEN '2025-01-10' AND '2025-01-12'
GROUP BY 1, 2;
```

* Cross-check against:

  * Raw event counts for a single country and day,
  * Known test users or synthetic data.

12. **Backfill & dashboard wiring**

* Run the new query over a historical window in a sandbox table.
* Wire the dashboard to that table or view:

  * Use a feature flag / config to switch from old to new query.

13. **Monitoring after deploy**

* Track:

  * Query latency,
  * Daily row counts vs historical ranges,
  * Known “anchor days” (e.g., holidays) to ensure relative shapes look correct.
* If anomalies appear, use the runbook to iterate:

  * Update filters/joins,
  * Re-run validation.

14. **Document assumptions**

* Time zone: all in UTC.
* Country mapping: based on `country_code` only.
* Out-of-scope decisions:

  * Multi-country users counted per country where they have events.
  * Refunds/negative amounts not modeled here (call out separately).

This runbook is structured, validation-focused, and performance-aware – what the Warden considers a strong answer.
