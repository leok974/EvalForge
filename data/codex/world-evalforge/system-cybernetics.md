---
id: system-cybernetics
title: Cybernetics (Skill Tree)
world: world-evalforge
tier: 1
tags: [meta, system, progression]
summary: Neural augmentations that unlock new capabilities.
source: curated
---

# System Overview
The **Cybernetics Lab** allows Architects to upgrade their interface. By spending Skill Points (SP) earned from leveling up, you can unlock new modules.

# Technical Specifications
- **Data Model:** `SkillNode` and `UserSkill` in Postgres.
- **Logic:** `skill_helper.py` validates dependencies (Parent/Child) and cost.
- **Frontend:** `useSkills` hook gates UI features (e.g. disabling the "Explain" button if `module_elara` is locked).
