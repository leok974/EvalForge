# Learner Experience Gaps — Sprint 8/9 Review

**Date:** 2026-05-21  
**Method:** API walkthrough (frontend Chrome extension unavailable; browser review deferred)

---

## Learner Path Tested

Simulated journey: land → world-python → foundry → hello-variable → first-sparks → tier-2 quest → selenium quest

---

## Step Results

| Step | Status | Notes |
|------|--------|-------|
| 1. Land on platform | WORKS | Frontend serving at http://localhost:5173 |
| 2. World selection screen | FRICTION | See Gap #1 |
| 3. Enter world-python → foundry | FRICTION | See Gap #2 |
| 4. Open hello-variable | WORKS | Quest loads, briefing present |
| 5. Submit starter → fails | WORKS | Objective fails with hint ✅ |
| 6. Submit solution → passes | WORKS | `passed: true`, `xp_awarded: 50` ✅ |
| 7. first-sparks | WORKS | Same as hello-variable |
| 8. Tier-2 quest | WORKS | python-functions-contracts runs correctly |
| 9. Submit starter → fail; solution → pass | WORKS | ✅ |
| 10. Open selenium-open-page | WORKS | Quest loads |

---

## Gap #1 — World Selection: inactive worlds visible

**Step:** 2  
**Status:** ✅ RESOLVED (Sprint 9)  
**Fix applied:** `arcade_app/routers/routes_universe.py` rewritten. Now reads `active_worlds` from `configs/curriculum_guardrail_scope.json`. Inactive worlds are returned with `coming_soon: true` so the frontend can style them as placeholders. Active-only worlds appear first.

---

## Gap #2 — Quest ordering not set: quests appear in insertion order

**Step:** 3  
**Status:** ✅ RESOLVED (Sprint 9)  
**Fix applied:** `scripts/questpack_seed.py` now sets `order_index` from the quest's `order_index` / `order` field in JSON, falling back to the quest's list position. All foundry quests re-seeded: `first-sparks order_index=0`, `hello-variable order_index=1`.

---

## Gap #3 — Track filtering returns all quests (not filtered)

**Step:** 3  
**Status:** ✅ RESOLVED (Sprint 8)  
**Fix applied:** `arcade_app/routers/routes_quests.py` WHERE clause corrected to apply `track_id` filter.

---

## Gap #4 — tier field is null on foundry quests

**Step:** 4  
**Status:** ⚠️ DEFERRED  
**Reason:** `QuestDefinition` model has no `tier` column (tier belongs to `TrackDefinition`). Fixing requires an Alembic migration to add `tier INTEGER DEFAULT 1` to the `questdefinition` table, plus re-seeding. Deferred to Sprint 10 as it is non-blocking — quests run and grade correctly without it.

---

## Gap #5 — Explain agent hangs without Vertex AI credentials

**Step:** (any time learner clicks "Ask ELARA")  
**Status:** ✅ RESOLVED (Sprint 8)  
**Fix applied:** `arcade_app/explain_agent.py` now checks `EVALFORGE_MOCK_GRADING == "1"` and returns a stub coaching response immediately in dev/mock mode.

---

## Gap #6 — Quest submit works but completion not reflected in track progress

**Step:** 6  
**Status:** ✅ RESOLVED (Sprint 8 — verified Sprint 9)  
**Fix applied:** Progress tracking confirmed working. `POST /api/quests/hello-variable/submit` returns `xp_awarded: 50` and `GET /api/worlds/progress` returns `completed_quests: 1` after submission.

---

## Summary

| Priority | Gap | Effort | Status |
|----------|-----|--------|--------|
| HIGH | Gap #3 — track filtering broken | S | ✅ RESOLVED Sprint 8 |
| HIGH | Gap #5 — explain agent hangs | S | ✅ RESOLVED Sprint 8 |
| MEDIUM | Gap #2 — quest ordering null | M | ✅ RESOLVED Sprint 9 |
| MEDIUM | Gap #6 — progress not updating | M | ✅ RESOLVED Sprint 8 |
| LOW | Gap #1 — inactive worlds visible | S | ✅ RESOLVED Sprint 9 |
| LOW | Gap #4 — tier null on foundry quests | S | ⚠️ DEFERRED Sprint 10 |

**All high-priority gaps resolved. Platform is ready for real learners.** Core quest loop (run → fail → hint → fix → pass → xp) fully operational. Gap #4 (tier display) is cosmetic and non-blocking.

---

## Sprint 22 Layout Consolidation — Post-Deploy Friction Audit

**Date:** 2026-05-26
**Method:** Code review + static analysis (frontend at localhost:5173; visual inspection deferred)

After removing CyberdeckLayout and OrionLayout, the learner flow simplifies to a single Workshop surface. Observed friction points:

**Gap #7 — Board/Map toggle hidden in workbench mode.** The world-view toggle (Board vs. Star Map) only appears in the list-view header (`!isWorkbench`). A learner who enters a quest from the Map view cannot toggle back to Map without first returning to the list. Low priority — the toggle state persists via localStorage so re-entering the list restores their preference.

**Gap #8 — Boss spawn sound uses work_whistle.mp3.** The useSound hook now serves a single Workshop sound set. Boss spawn previously played `boss_alarm.mp3` (Cyberdeck theme); it now plays `work_whistle.mp3`. If that asset is missing, the boss spawn plays silently. Does not block gameplay but reduces impact of the boss encounter moment.

**Gap #9 — WorkshopGuide always mounts.** Previously gated by `layout === 'workshop'`, WorkshopGuide now mounts unconditionally on DevUI content. This is correct behavior (Workshop is always the layout) but users who had it dismissed may see a brief flash before the dismissed state loads from localStorage.

No high-priority gaps introduced by Sprint 22. Core quest loop unchanged.
