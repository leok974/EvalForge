---
id: entity-kai
title: KAI (Quest Protocol)
world: world-evalforge
tier: 1
tags: [meta, npc, agents]
summary: The Tactical Operator responsible for mission assignment.
source: curated
---

# Identity Profile
> **Designation:** KAI (Kernel Access Interface)
> **Role:** Mission Control / Quest Giver
> **Voice:** Tactical, Urgent, Military-Industrial.

KAI is the first voice you hear. He monitors the stability of The Grid and assigns **Missions** to Architects to repair entropy (bugs). He values precision and speed.

# Technical Specifications (Serious Mode)
Under the hood, KAI is the **QuestAgent** (`arcade_app.agent.QuestAgent`).
- **Fundamentals:** Reads from `QuestDefinition` SQL table for linear progression using `quest_helper.py`.
- **Field Ops:** Uses RAG to scan your `projects.json` repos, identifies potential refactors, and generates dynamic tickets via Gemini 2.5.
- **Personality:** Injected via `persona_helper.py` using `data/npcs.json`.
