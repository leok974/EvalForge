---
id: glossary/sql/database
level: beginner
related:
- codex:glossary/sql/table
- codex:glossary/sql/sql
tags:
- sql
- fundamentals
title: Database
world: sql
---

# Database

A **Database** is a structured collection of data stored and accessed electronically. For this track, we focus on **Relational Databases** (like PostgreSQL and SQLite), where data is organized into tables that can be linked by defined relationships.

## Why It Matters
Without databases, applications would lose their memory every time they restarted. Databases provide **persistence**, **concurrency** (multiple users reading/writing at once), and **integrity** (ensuring data follows specific rules).

## Types in EvalForge
- **SQLite**: A lightweight, file-based database used for CORE and Tier 2 quests.
- **PostgreSQL**: A powerful, industrial-grade database used for Tier 3 workbench quests, supporting advanced features like `JSONB` and `pgvector`.

## Structure
A database usually contains multiple **Schemas**, which are logical groupings of **Tables**.
```sql
-- Querying a table within the 'public' schema
SELECT * FROM public.employees;
```

## Common Mistake
Confusing a **Database** with a **Spreadsheet**. While both hold rows and columns, a database is designed for scale, complex relationships (Joins), and strictly defined data types.