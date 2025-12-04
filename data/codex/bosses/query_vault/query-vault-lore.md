---
slug: boss-query-vault-lore
boss_id: query_vault
tier: 1
world_id: world-archives
tags:
  - boss
  - query_vault
  - lore
  - sql
  - analytics
title: "The Query Vault – System Briefing"
---

> KAI: "The data is here. The problem is *you*."

## Narrative Brief

The **Query Vault** is the first major boss of **THE ARCHIVES (world-sql)**.

In-universe, it guards a cluster of reporting tables:

- `users`, `sessions`, `events`, `plans`, `payments`, …
- All correctly modeled—but not always clean.
- Some rows missing, some timestamps misaligned, some foreign keys optional.

Your job is to write **precise, robust SQL** that unlocks a set of analytics questions:

- Activation metrics,
- Conversion funnels,
- Retention windows,
- Revenue breakdowns.

**What this boss is testing:**

- Can you translate **plain English questions** into **correct SQL**?
- Do you understand how to combine **JOIN + GROUP BY + filters** safely?
- Can you handle **NULLs and missing data** without lying to yourself?

## The Shape of the Fight

You are given:

- A schema diagram (or textual description) for a small analytics warehouse.
- A list of canonical questions (e.g. activation rate by plan, revenue by cohort).
- A starting stub for queries or a query builder function.

You will face:

- Datasets with **intentional edge cases**: missing foreign keys, sparse events.
- Tests that compare your query outputs to expected result sets.
- Hidden cases where sloppy joins return *neatly wrong* aggregates.

## Why It Matters

Many engineers can read logs. Fewer can write:

- A **single, clean query** that answers a business question.
- A query that **doesn't silently double-count**.
- A query that is **fast enough** to run regularly.

The Query Vault is where EvalForge checks if you’re ready to talk to analysts without breaking their dashboards.

## Intel From Previous Units

> ZERO: "Most Units pass on 'toy' examples and then fail once real NULLs show up."

Common failure patterns:

- Using `INNER JOIN` where `LEFT JOIN` is required.
- Forgetting to filter to the right time windows.
- Grouping by too many columns and fragmenting metrics.
- Treating `NULL` as “0” without thinking about what it means.
