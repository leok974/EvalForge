# EvalForge — Claude Code Reference

## What This Project Is

EvalForge is an interactive engineering mastery platform built around gamified "quests." Learners select a world, pick a quest, write code in the embedded IDE, run it against real execution environments (Postgres, Selenium, Python), and receive structured feedback: console output, objective results, automation traces, and codex doc links. The goal is mentor-level practical skill in SQL, Python, Selenium, testing, and automation.

---

## Repository Layout

```
arcade_app/          Backend: FastAPI app, LangGraph agents, quest runners, DB models
apps/web/            Frontend: React + TypeScript Vite SPA (cyberdeck UI)
data/
  questpacks/        Quest content packs (JSON, ~44 files)
  worlds.json        World definitions
  tracks.json        Track definitions
  seed/              active_curriculum.json, skilltree.json
configs/
  curriculum_guardrail_scope.json   Active scope enforcement
  questpacks_active.json            Canonical active packs list
  quest_exclusions.json             Excluded quests (with reason/date)
  tutorial_policy.json              Tutorial visibility rules
docs/
  codex/             Markdown knowledge base (glossaries, guides)
  audits/            Verification snapshots and reports
runtimes/
  python/selenium/   Selenium runner: runner.py, browser.py, harness.py, step_logger.py
scripts/             280+ audit, seed, verify, and dev scripts
solutions/           Reference solutions by world/track/quest
rubrics/             Boss evaluation rubrics (JSON)
tests/
  backend/           pytest suite (100+ files)
  e2e/               Playwright smoke tests
migrations/          Alembic DB migrations
```

---

## Local Development

### Full stack (Docker — preferred)
```powershell
.\scripts\dev-up.ps1
```
Starts all containers, waits for health checks, tails logs.
- Frontend: http://localhost:5173
- Backend:  http://localhost:8092
- API docs: http://localhost:8092/docs

### Backend only (hot-reload, requires DB + Redis already running)
```powershell
.\scripts\dev-api.ps1
```
Connects to Postgres on `127.0.0.1:5435` and Redis on `127.0.0.1:6380`.

### Frontend only
```bash
cd apps/web && npm run dev
```

### Environment variables (copy `.env.example` → `.env`)
```
POSTGRES_PASSWORD=...
GOOGLE_CLOUD_PROJECT=...
GOOGLE_CLOUD_LOCATION=us-central1
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
SECRET_KEY=...
```
Backend also uses `DATABASE_URL`, `REDIS_URL`, `EXECUTION_ENABLED`, `AUTO_INIT_DB` — set automatically by dev scripts.

---

## Backend Architecture

**Entry point:** `arcade_app/agent.py` (main FastAPI app, ~700 lines)

**Key modules:**
| File | Purpose |
|------|---------|
| `arcade_app/models.py` | SQLModel table definitions (User, Quest, Boss, Codex, etc.) |
| `arcade_app/database.py` | Async Postgres + pgvector setup |
| `arcade_app/routers/routes_quests_runtime.py` | Quest code execution |
| `arcade_app/routers/routes_quests.py` | Quest CRUD and submission |
| `arcade_app/quest_agent_graph.py` | LangGraph quest evaluation graph |
| `arcade_app/explain_agent.py` | Socratic coaching agent |
| `arcade_app/questmaster.py` | Quest catalog and management |
| `arcade_app/config.py` | Environment config |

**AI stack:** Google Vertex AI (Gemini 2.5) via LangGraph. Model references live in `arcade_app/llm.py`.

**Async jobs:** ARQ worker backed by Redis for boss fight events and background ingestion.

---

## Frontend Architecture

**Entry point:** `apps/web/src/App.tsx`
**Main interface:** `apps/web/src/pages/DevUI.tsx`

**Key component areas:**
- `components/quests/` — QuestIDE, BriefingCard, QuestDrawer, QuestResultPanel
- `components/codex/` — CodexDrawer, codex lookup
- `components/hud/` — ActiveTrackStatus, EventLog, NetworkPanel
- `features/` — Zustand state slices (quests, boss, progress, workshop)

**Build:** Vite 5.4, React 19, TypeScript 5.6, Tailwind CSS 3.4

---

## Quest Content System

Quest content lives in `data/questpacks/*.json`. Each questpack defines a group of quests for a world/track.

Individual quest workspace files live under `data/quests/<slug>/`:
```
workspace/   main.py, example.py, task.py (learner files)
solution/    solution.py (reference)
docs/        tutorial.md, briefing.md, hints.md, lore.md
```

After editing questpacks, seed to the DB:
```bash
# For data/questpacks/*.json files (canonical seeder):
docker compose exec backend bash -c "cd /app && PYTHONPATH=/app python scripts/questpack_seed.py data/questpacks/<file>.json"
# Or to seed all active packs at once:
docker compose exec backend bash -c "cd /app && PYTHONPATH=/app python scripts/questpack_seed.py --all"

# For legacy world/track specs (docs/*.json):
python scripts/seed_evalforge_universe.py
```

**NOTE:** `questpack_seed.py` is the correct seeder for all `data/questpacks/*.json` files. `seed_evalforge_universe.py` only processes legacy track specs in `docs/` — it does NOT process `sql_core.json`, `javascript_core.json`, etc.

---

## Active Curriculum Scope

Defined in `configs/curriculum_guardrail_scope.json`:
- **Active worlds:** `world-python`
- **Active tracks:** `track-python-systems`, `track-python-ignition`, `track-python-foundry`, `track-python-selenium`
- **Warning-only worlds:** `world-sql`, `world-js`, `world-ts`, `world-web`

CI enforces training-grade quality only for active scope. Other worlds produce warnings but do not block.

---

## Selenium / Mock CMS

The Selenium runner in `runtimes/python/selenium/` drives headless Chrome against the Mock CMS (a local Flask/FastAPI web app simulating real browser automation scenarios). Routes: `/login`, `/dashboard`, `/search`, `/latency`, `/modals`, `/tickets`, `/refresh`.

**App Preview** (in the IDE) is a visible iframe sandbox — not the Selenium browser. The Selenium browser runs headlessly in the runner.

**Automation Trace:** Selenium scripts emit structured step logs parsed from stdout sentinels. The trace appears in the frontend after a run and shows each step's pass/fail status.

Codex docs for Selenium:
- `docs/codex/glossary/python/selenium-webdriver.md`
- `docs/codex/glossary/python/selenium-explicit-waits.md`
- `docs/codex/guides/selenium/debugging.md`

---

## Verification and CI

### Verify all active worlds
```bash
python scripts/verify_all_modern_worlds.py
```
Outputs to `docs/audits/FINAL_SWEEP_VERIFICATION.md`.

### CI regression guard
```bash
python scripts/ci_check_modern_worlds.py
```
Enforces against `docs/audits/TRAINING_GRADE_SNAPSHOT.json`:
- Solution mode: must be 100% passing
- Student mode: must match snapshot state exactly

### Curriculum validator
```bash
python scripts/certify_training_grade.py
```
Checks schema compliance, placeholder text, broken Codex refs, missing docs, workspace completeness.

### Population audit
```bash
python scripts/audit_all_worlds.py
```
Compares source questpacks → seeded DB → API-visible quests → UI-visible quests.

---

## Testing

```powershell
# Backend tests
pytest tests/backend/

# Frontend tests
cd apps/web && npm run test

# E2E smoke
cd apps/web && npx playwright test tests/e2e/
```

---

## Common Scripts

| Script | Purpose |
|--------|---------|
| `scripts/dev-up.ps1` | Start full Docker stack |
| `scripts/dev-api.ps1` | Start backend with hot-reload |
| `scripts/seed_evalforge_universe.py` | Seed worlds/tracks/quests to DB |
| `scripts/seed_bosses.py` | Seed boss definitions |
| `scripts/ingest_codex.py` | Index codex docs into pgvector |
| `scripts/init_local_db.py` | Initialize local DB schema |
| `scripts/audit_codex_refs.py` | Audit broken codex key-term references |
| `scripts/debt_breakdown.py` | Report on curriculum tech debt |

---

## Key Design Decisions

- **Scoped enforcement:** Active worlds/tracks block CI on quality failures; warning-only worlds never block. Never tighten guardrails on inactive scope without updating `curriculum_guardrail_scope.json` first.
- **Seed scripts must upsert:** Seeding always updates existing rows. Never write seed scripts that only insert — this causes silent drift between source files and the DB.
- **Editor failure targeting:** Runtime errors target exact lines from tracebacks. Objective failures use heuristic region targeting (anchors, TODO comments, function regions) — they must never overclaim precision.
- **Mock CMS uses PRG:** Login route uses Post-Redirect-Get so Selenium URL-wait assertions work correctly. Do not change this to render-on-POST.
- **Quest exclusions are structured:** `configs/quest_exclusions.json` requires `reason`, `added_at`, and `owner` fields. Older exclusions escalate from warning to failure automatically.
- **Example file run parity:** Running `example.py` must execute `example.py`, not `main.py`. The runner selects the file based on the active editor tab, not a hardcoded entrypoint.

---

## Cleanup Policy

Rules for keeping the repo clean. Apply these before adding or deleting anything in the affected areas.

- **One-off scripts get deleted, not archived.** If a script is a migration, fix, patch, or backfill that has already run, delete it after confirming it is not called by anything. Do not move it to an `_archive/` folder or rename it with a `.done` suffix — that just defers the problem.
- **`configs/questpacks_active.json` is the validity gate for questpack tooling.** The CI sweep script (`verify_all_modern_worlds.py`) reads this file directly. Do not add questpack verification logic that globs `data/questpacks/` — any new pack must be explicitly listed in `questpacks_active.json` before it is tested.
- **Audit snapshots supersede old reports.** `docs/audits/TRAINING_GRADE_SNAPSHOT.json` is the canonical CI baseline. Phase/sweep markdown reports in `docs/audits/` are point-in-time artifacts. Delete them once the snapshot covers the same scope — do not let them accumulate.
- **Routers must be registered to exist.** An APIRouter that is not mounted in `agent.py` is dead code. If a router file is intentionally kept for future work, annotate it with a `# STATUS: unregistered` comment at the top. If it has no annotation and is not mounted, it is a deletion candidate.
