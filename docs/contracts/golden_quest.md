# 🏆 Golden Quest Contract

This document defines the formal quality standards for a **Golden Quest** in EvalForge. Quests meeting this standard are eligible for the "Golden" tag and are prioritized in the curriculum.

## 1. Metadata Standards
All Golden Quests must have complete and accurate metadata:
- **`title`**: Descriptive and engaging.
- **`short_description`**: Concise summary of the learning objective.
- **`world_id` & `track_id`**: Valid references to existing worlds and tracks.
- **`objectives`**: A structured list of actionable goals.

## 2. Instructional Content
The quest experience must be rich and self-contained:
- **Briefing**: Clear lore-aligned mission description.
- **Tutorial**: Step-by-step guidance with syntax-highlighted code blocks.
- **Hints**: At least 2-3 progressive hints for the challenge.
- **Key Terms**: At least 3 relevant glossary terms attached.

## 3. Workspace & Files
- **Starter/Task Files**: Functional boilerplate for the learner.
- **Example File (`example.py` / `example.sql`)**: A runnable reference implementation that demonstrates the target concept.
- **Reference Parity**: The example output should align with the tutorial's expected behavior.

## 4. UX & Rendering
- **Workshop Visibility**: Description and title must render correctly in the catalog.
- **Content Richness**: Tutorial must have meaningful prose (not placeholders).
- **Run Experience**: The "Run this file" affordance must work for example files.
- **Execution Labels**: Terminal output should be clearly labeled (e.g., `--- Running example.py ---`).

## 5. Automated Guardrails
Golden Quests are subject to **Tier 2 (Active Scope)** enforcement:
- **Warning**: Triggered if non-metadata content (e.g., hints) is missing.
- **Failure**: CI blocks if structural metadata is missing or if the quest has been excluded for > 90 days.
- **Smoke Tests**: Playwright must verify successful navigation and execution for active quests.

## 6. Maintenance & Aging
- Exclusions of Golden Quests in `quest_exclusions.json` are temporary.
- **30 Days**: Warning issued for a persistent exclusion.
- **90 Days**: Hard failure in CI to prevent quality debt from accumulating.
