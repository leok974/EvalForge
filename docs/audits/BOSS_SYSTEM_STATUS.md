# Boss Fight System — Status Audit

**Date:** 2026-05-21  
**Sprint:** 8  
**Verdict:** OPERATIONAL

---

## Architecture

The boss fight system is fully wired into the running backend:

| Layer | File | Status |
|-------|------|--------|
| Routes | `arcade_app/routers/routes_boss.py` | ✅ Mounted in `agent.py` |
| DB Models | `arcade_app/models.py` — `BossDefinition`, `BossEncounter`, `BossRun` | ✅ Schema present |
| Encounter logic | `arcade_app/boss_helper.py` — `create_encounter`, `get_active_encounter`, `resolve_boss_attempt` | ✅ Implemented |
| Grading | `arcade_app/grading_helper.py` — `judge_boss_submission` | ✅ Implemented |
| Rubrics | `rubrics/*.json` — 5 boss rubric files | ✅ Present |
| Seed script | `scripts/seed_bosses.py` | ✅ Present |
| Mock grading | `EVALFORGE_MOCK_GRADING=1` in `.env` | ✅ Active |

## Endpoints

| Endpoint | Method | Behavior |
|----------|--------|----------|
| `/api/boss/current` | GET | Returns `{"active": false}` when no encounter exists |
| `/api/boss/accept` | POST | Creates encounter — requires seeded `BossDefinition` |
| `/api/boss/submit` | POST | Calls `judge_boss_submission` → mock grader active in dev mode |
| `/api/boss/history` | GET | Returns encounter history |

## End-to-End Test Results (Sprint 8)

**Tested with:** `boss_id: "reactor-core"`, mock mode: YES (`EVALFORGE_MOCK_GRADING=1`)

| Step | Request | Response |
|------|---------|----------|
| 1 | `GET /api/boss/current` | `{"active": false}` ✅ |
| 2 | `POST /api/boss/accept {"boss_id":"reactor-core"}` | `{"encounter_id": N, "boss_name": "The Reactor Core", ...}` ✅ |
| 3 | `POST /api/boss/submit {"encounter_id":N, "code":"print('hello')"}` | `{"status":"loss","score":45,...}` ✅ |
| 4 | `POST /api/boss/submit {"encounter_id":N, "code":"MAGIC_BOSS_PASS = True"}` | `{"status":"win","score":100,...}` ✅ |

**Learner-facing output shape:**
```json
{
  "status": "win",
  "score": 100,
  "xp_awarded": 1000,
  "encounter_id": 1,
  "boss_name": "The Reactor Core",
  "time_taken_seconds": <int>
}
```

Loss response uses same shape with `"status": "loss"` and `"score": 45`.

## Mock Grader Behavior

`EVALFORGE_MOCK_GRADING=1` activates `arcade_app/mock_grader.py`:
- Default: returns score `45` → `status: "loss"`
- If `"MAGIC_BOSS_PASS"` appears in submitted code: returns score `100` → `status: "win"`

## Seeded Boss Definitions

| ID | Name | Max HP | Time Limit | XP |
|----|------|--------|------------|-----|
| `reactor-core` | The Reactor Core | 3 | 1800s (30 min) | 1000 |

Seed command:
```bash
docker compose exec backend bash -c "cd /app && PYTHONPATH=/app python scripts/seed_bosses.py"
```

## SQL Tier-3 — Quest Status

The `sql_tier3.json` pack contains 10 quests. Status as of Sprint 8:

| Quest | Status | Notes |
|-------|--------|-------|
| `postgres-schema-explorer` | PASS (3/3) | SQLite-compatible test written, passes in CI |
| `postgres-real-schema-joins` | STUB_ONLY | No grading directory — requires Postgres fixture authoring |
| `postgres-safe-querying` | STUB_ONLY | No grading directory — requires Postgres fixture authoring |
| `postgres-date-trunc-time-buckets` | STUB_ONLY | No grading directory — requires Postgres fixture authoring |
| `postgres-explain-basics` | STUB_ONLY | No grading directory — requires Postgres fixture authoring |
| `postgres-jsonb-basics` | STUB_ONLY | No grading directory — requires Postgres fixture authoring |
| `sql-vector-q1-mental-model` | EXCLUDED (STUB) | No objective kind — in `quest_exclusions.json` |
| `sql-vector-q2-distance-metrics` | EXCLUDED (STUB) | No objective kind — in `quest_exclusions.json` |
| `sql-vector-q3-top-k-retrieval` | EXCLUDED (STUB) | No objective kind — in `quest_exclusions.json` |
| `sql-vector-q4-hybrid-search` | EXCLUDED (STUB) | No objective kind — in `quest_exclusions.json` |

`postgres-schema-explorer` now passes with a SQLite-compatible test (`data/quests/postgres-schema-explorer/grading/public/test_postgres_schema_explorer.py`). The remaining 5 postgres quests are STUB_ONLY — they have workspace content but no `grading/` directory and require live Postgres fixture infrastructure not yet in the CI pipeline.
