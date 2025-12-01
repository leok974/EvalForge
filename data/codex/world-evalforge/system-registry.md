---
id: system-registry
title: The Registry (Project Ops)
world: world-evalforge
tier: 1
tags: [meta, system]
summary: How to manage your linked repositories via KAI.
source: curated
---

# System Overview
The **Registry** is the database of external realities (GitHub Repositories) linked to The Construct.

# Interaction Protocols
You can interact with the Registry in two ways:
1.  **Visual Interface:** The "Projects" dashboard (Top Menu).
2.  **Command Line:** By entering the **Project Registry** track, you can issue direct orders to **KAI**.

# Commands
- "List projects" -> Displays status of all links.
- "Sync [name]" -> Triggers re-ingestion of a specific repo.
- "Add [url]" -> Links a new repo.

# Technical Specifications
KAI uses the `REGISTRY_TOOLS` set via LangGraph to execute CRUD operations on the `Project` SQL table.
