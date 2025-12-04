---
slug: boss-query-vault-strategy
boss_id: query_vault
tier: 3
world_id: world-archives
tags:
  - boss
  - query_vault
  - strategy
  - sql
  - analytics
title: "The Query Vault – Strategy & Survival Guide"
---

> ELARA: "The Vault does not need cleverness. It needs honesty."

You unlocked this by defeating the Query Vault.  
Here is the strategy guide.

---

## 1. Write the Question Like an Analyst

Before you write SQL:

1. Rewrite the question in plain language:
   - "Activation rate = users who did X within Y days / all new users in that period."
2. Identify:
   - **Grain**: user, session, event, plan, etc.
   - **Time anchor**: user creation, event timestamp, billing date.

Then design the query at that grain first.

---

## 2. Pick the Right Grain and Build Up

For each metric:

- Decide the **base table / grain** (e.g. `users` for activation).
- Attach other tables via **LEFT JOIN**s with careful ON conditions.
- Push filters where they belong:

  - Event-type filters in event subqueries.
  - Plan status filters in the plan dimension.

Use CTEs to make intent clear:

```sql
WITH activated_users AS (
  SELECT DISTINCT e.user_id
  FROM events e
  WHERE e.name = 'activated'
    AND e.ts <= u.created_at + INTERVAL '7 days'
)
SELECT
  ...
FROM users u
LEFT JOIN activated_users a ON a.user_id = u.id;
```

---

## 3. Beware Multiplication

Always ask:

> "Does this join multiply rows for my chosen grain?"

If yes:

* Either aggregate in a subquery first,
* Or adjust grouping so you don't double-count.

Example:

```sql
WITH payments_per_user AS (
  SELECT user_id, SUM(amount) AS total_revenue
  FROM payments
  GROUP BY user_id
)
SELECT ...
FROM users u
LEFT JOIN payments_per_user p ON p.user_id = u.id;
```

---

## 4. Treat NULLs and Missing Rows Deliberately

Use:

* `COALESCE` when you really mean "default to 0",
* Conditional logic when missing relationships signal a distinct category (e.g. “never activated”).

Check each NULL:

* Is it *no data*, or *a meaningful absence*?
* Does it belong in the denominator?

---

## 5. Lock In Time Windows

Always write OUT the window conditions like a small truth table:

* `start <= ts < end` is often better than inclusive/inclusive.
* Be explicit about timezone, especially if your data mixes `TIMESTAMP WITH TIME ZONE` and `WITHOUT`.

Wrap that into named CTEs or comments so future-you and teammates can read it.

---

> ELARA: "Once you can reason at the level of grain, windows, and joins, SQL stops being a guessing game. The Vault stops being scary. It just becomes a locked door with a perfectly reasonable key."
