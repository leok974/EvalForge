---
id: system-ingestion
title: Project Ingestion (The Bridge)
world: world-evalforge
tier: 2
tags: [meta, system, rag]
summary: The mechanism for assimilating external codebases.
source: curated
---

# System Overview
**The Bridge** connects The Construct to external Git repositories. It scans, maps, and indexes code so Agents can understand your personal projects.

# Technical Specifications
- **Worker:** `ingestion_helper.py` runs in a background thread/worker.
- **Clone:** Uses `GitPython` to shallow clone repos to temp dirs.
- **Map:** Generates a virtual `PROJECT_MAP.md` tree structure.
- **Vector:** Chunks files and embeds them using `text-embedding-004` into `pgvector`.
- **Events:** Broadcasts progress via Redis Pub/Sub (`sync_progress`).
