---
id: glossary/sql/sql
level: beginner
related:
- codex:glossary/sql/database
- codex:glossary/sql/query
tags:
- sql
- fundamentals
title: SQL
world: sql
---

# SQL (Structured Query Language)

**SQL** is the universal domain-specific language used to communicate with Relational Database Management Systems (RDBMS). It allows users to define data structures, manipulate records, and query information efficiently.

## Why It Matters
In the era of Big Data, SQL remains the most critical skill for data analysts, engineers, and scientists. It provides a declarative way to ask questions ("What is the total revenue?") rather than explaining the step-by-step logic of how to get the data.

## Core Capabilities
- **DQL (Data Query Language)**: Fetching data using `SELECT`.
- **DDL (Data Definition Language)**: Defining structures using `CREATE`, `ALTER`, and `DROP`.
- **DML (Data Manipulation Language)**: Modifying data using `INSERT`, `UPDATE`, and `DELETE`.
- **DCL (Data Control Language)**: Managing permissions using `GRANT` and `REVOKE`.

## Basic Example
A simple "Hello World" of SQL involves selecting a literal value or a calculation:
```sql
SELECT 1 + 1 as results;
```

To fetch specific information from a table:
```sql
SELECT name, email 
FROM users 
WHERE status = 'active';
```

## Common Mistake
Treating SQL like a procedural language (looping over rows). SQL is **set-based**; it works best when you think about transformations on entire sets of data at once.