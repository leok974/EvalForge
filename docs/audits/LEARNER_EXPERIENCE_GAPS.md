# Learner Experience Gaps — Sprint 8 Review

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
**What happens:** `GET /api/universe` returns 3 worlds — world-python, world-sql, and world-agents.  
world-sql and world-agents are warning-only in `curriculum_guardrail_scope.json` (not active scope).  
**What should happen:** Only world-python should be prominently displayed. Other worlds should be marked "Coming Soon" or hidden.  
**Effort:** S  
**Fix action:** Filter `GET /api/universe` or add `enabled: bool` to world records, or handle in frontend with a world allowlist. `configs/curriculum_guardrail_scope.json` already defines `active_worlds: ["world-python"]`.

---

## Gap #2 — Quest ordering not set: quests appear in insertion order

**Step:** 3  
**What happens:** All 166 quests have `order: null`. Within a track, quests are returned in DB insertion order which doesn't match the intended learning progression.  
**What should happen:** `first-sparks` → `hello-variable` → tier-2 quests in deliberate sequence.  
**Effort:** M  
**Fix action:** Add `order` field population to `questpack_seed.py` (use the quest's list position in the JSON file as its order index). No schema migration needed — `order` column exists but is null.

---

## Gap #3 — Track filtering returns all quests (not filtered)

**Step:** 3  
**What happens:** `GET /api/quests?track_id=python-fundamentals` returns 166 quests (same as no filter). `GET /api/quests?track_id=track-python-foundry` also returns 166. Track filtering is broken or ignored in the routes_quests handler.  
**What should happen:** Only the 2 foundry quests should appear when filtering by `track_id=python-fundamentals`.  
**Effort:** S  
**Fix action:** Read `arcade_app/routers/routes_quests.py` and confirm the `track_id` query param is being applied to the DB query. If it's a WHERE clause issue, add `.where(QuestDefinition.track_id == track_id)` filter.

---

## Gap #4 — tier field is null on foundry quests

**Step:** 4  
**What happens:** `first-sparks` and `hello-variable` have `tier: null` in the API (should be `tier: 1`).  
**What should happen:** `tier: 1` so the UI can use tier for gating, visual styling, or sorting.  
**Effort:** S  
**Fix action:** Check `questpack_seed.py` — the foundry questpack JSON uses field name `tier` at quest level, but the seeder may not map it. Add `tier` to the field mapping in the seed script.

---

## Gap #5 — Explain agent hangs without Vertex AI credentials

**Step:** (any time learner clicks "Ask ELARA")  
**What happens:** `POST /api/agent/query/stream` with `mode: "explain"` returns HTTP 200 then streams 0 bytes — the SSE stream hangs indefinitely waiting for Vertex AI.  
**What should happen:** Without credentials, return an immediate error event explaining AI coaching is unavailable, or mock it similarly to `EVALFORGE_MOCK_GRADING=1`.  
**Effort:** S  
**Fix action:** In `arcade_app/explain_agent.py`, check `EVALFORGE_MOCK_GRADING == "1"` before calling `get_chat_model()`. Return a stub response: `"ELARA is offline in dev mode. Check your solutions and try the hint."`.

---

## Gap #6 — Quest submit works but completion not reflected in track progress

**Step:** 6  
**What happens:** `POST /api/quests/hello-variable/submit` returns `{"ok": true, "xp_awarded": 50}`. However `GET /api/worlds/progress` returns `completed_quests: 0` for all tracks (progress not updated).  
**What should happen:** After submitting, the foundry track shows 1/2 quests completed.  
**Effort:** M  
**Fix action:** Check `routes_quests.py` submit handler — confirm it writes a `quest_progress` record to the DB and that `routes_world_progress.py` reads from the same table.

---

## Summary

| Priority | Gap | Effort |
|----------|-----|--------|
| HIGH | Gap #3 — track filtering broken | S |
| HIGH | Gap #5 — explain agent hangs | S |
| MEDIUM | Gap #2 — quest ordering null | M |
| MEDIUM | Gap #6 — progress not updating | M |
| LOW | Gap #1 — inactive worlds visible | S |
| LOW | Gap #4 — tier null on foundry quests | S |

**Most critical friction point:** Track filtering is broken — learners see all 166 quests instead of the 2–10 quests in their current track, making navigation impossible without external guidance.

---

## Platform Readiness Verdict

**Not ready for real learners until Gap #3 (track filtering) and Gap #5 (explain agent hang) are fixed.** Both are S-effort fixes. The core quest loop (run → fail → hint → fix → pass → xp) is fully operational.
