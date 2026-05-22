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

### Environment variables

`.env.dev` is committed to the repo with safe placeholder values. It is the canonical starting point for local development.

```powershell
# First-time setup (or after deleting .env):
cp .env.dev .env
# Then fill in the real secrets (GEMINI_API_KEY, GITHUB_CLIENT_*, GOOGLE_CLOUD_PROJECT, etc.)
```

`dev-up.ps1` copies `.env.dev` → `.env` automatically when `.env` is missing, so on a fresh clone just run `.\scripts\dev-up.ps1` and it will bootstrap itself.

**Security rule:** `.env.dev` must NEVER contain real secrets. `GEMINI_API_KEY`, `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, `VERTEX_PROJECT_NUMBER`, and `GOOGLE_CLOUD_PROJECT` must remain empty (placeholder) in `.env.dev`. Real values go in `.env` only — which is gitignored.

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

### Quest Tier System
Quest difficulty is stored in the `tier` column on `QuestDefinition` (added Sprint 10 via migration 007):
- `tier=1` — Foundry (beginner)
- `tier=2` — Advanced / Ignition
- `tier=3` — Expert (postgres-specific, SQL tier 3)

Tier 2+ quests are certified with stricter rules: min 2 objectives, min 3 key_terms with valid Codex refs. Boss quests in tier 2+ require min 4 objectives.

### Boss Fights
Boss definitions are in the `bossdefinition` table. Rubric JSON files live in `rubrics/`. To seed bosses:
```bash
docker compose exec backend bash -c "cd /app && PYTHONPATH=/app python scripts/seed_bosses.py"
```
The `rubrics/` directory is mounted into the backend container as `/app/rubrics/` (docker-compose volume). The `_load_rubric()` helper in `seed_bosses.py` reads rubric JSON at seed time.

Active boss for world-python: `boss-foundry-systems-architect` (rubric: `rubrics/boss-foundry-systems-architect.json`).

---

## Active Curriculum Scope

Defined in `configs/curriculum_guardrail_scope.json`:
- **Active worlds:** `world-python`, `world-web`, `world-sql`, `world-js`, `world-ts`, `world-git`
- **Active tracks:** `track-python-systems`, `track-python-ignition`, `track-python-foundry`, `track-python-selenium`, `track-html`, `track-css`
- **Warning-only worlds:** _(none — all worlds are either active or excluded)_

CI enforces training-grade quality only for active scope. Other worlds produce warnings but do not block.

---

## Boss Fight System

Status as of Sprint 8: **OPERATIONAL** (mock grading active in dev).

**Flow:**
1. `POST /api/boss/accept {"boss_id":"reactor-core"}` — creates a `BossEncounter`
2. `POST /api/boss/submit {"encounter_id":N, "code":"..."}` — grades via `judge_boss_submission`
3. Response: `{"status":"win"|"loss", "score":0-100, "xp_awarded":N, ...}`

**Dev setup (required before first use):**
```bash
# 1. Seed boss definitions (one-time)
docker compose exec backend bash -c "cd /app && PYTHONPATH=/app python scripts/seed_bosses.py"

# 2. Enable mock grading in .env
EVALFORGE_MOCK_GRADING=1
```

**Mock grader behavior** (`EVALFORGE_MOCK_GRADING=1`):
- Any code → score 45 → `status: "loss"`
- Code containing `MAGIC_BOSS_PASS` → score 100 → `status: "win"`

**Key files:**
| File | Purpose |
|------|---------|
| `arcade_app/routers/routes_boss.py` | Boss fight endpoints |
| `arcade_app/boss_helper.py` | Encounter creation, HP resolution |
| `arcade_app/grading_helper.py` | `judge_boss_submission` — real + mock paths |
| `arcade_app/mock_grader.py` | Mock grader logic |
| `scripts/seed_bosses.py` | Seeds `BossDefinition` records |
| `rubrics/*.json` | Boss evaluation rubrics |
| `docs/audits/BOSS_SYSTEM_STATUS.md` | Full audit with test results |

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
Checks schema compliance, broken Codex refs, tier compliance, and golden artifact coverage.
**Scope-aware:** only active questpacks (from `configs/curriculum_guardrail_scope.json`) produce hard failures. Non-active quests emit `[WARN]` but do not fail the run.
Requires `libcst` (in `requirements.txt`) for the drift check sub-step.

### Population audit
```bash
python scripts/audit_all_worlds.py
```
Compares source questpacks → seeded DB → API-visible quests → UI-visible quests.

### Cherry-pick safety guard
```bash
python scripts/check_cherry_pick_diff.py <SHA>
```
Detects top-level function and class deletions in a commit before it is cherry-picked to a protected branch. Exit 0 = clean, exit 1 = deletions found.

**Limitation:** `check_cherry_pick_diff.py` detects top-level function/class deletions only (lines starting at column 0 with `def `, `async def `, or `class `). Indented method removals inside a class body are not currently detected. If a commit removes a class method (e.g. `    def my_method(self):`), the guard will not flag it. Be aware of this gap when reviewing commits that modify class internals.

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

### Pre-existing test failures

**Any test that has been failing across more than 2 sprints must be classified as FIX, DELETE, or SKIP within the current sprint. "Pre-existing failing" is not a permanent state.**

This rule is **mechanically enforced** by `scripts/audit_skipped_tests.py`, which runs as part of `scripts/ci_check_modern_worlds.py`. Adding a `test.skip()` without the required comment format will cause CI to fail once the revisit sprint passes.

Classification rules:
- **FIX** — the underlying feature exists and the test is repairable (wrong selector, URL change, etc.)
- **DELETE** — the feature/route no longer exists and will not come back
- **SKIP** — the test covers real functionality but is blocked by a known issue; add a `test.skip()` with a comment in this exact format:
  ```typescript
  test.skip('...', async ({ page }) => {
      // SKIP: <one-line reason>
      // Blocker: <specific implementation gap and the file(s) that would change>
      // Revisit: Sprint N
  ```
- **PORT** — the test is correct but belongs in a different file or test framework

The audit script reads `configs/current_sprint.txt` for the current sprint number. Update that file at the start of each sprint. Any SKIP whose `Revisit: Sprint N` target is ≤ current sprint will fail CI until the skip is re-classified.

### Monaco editor interactions in Playwright

- **Never use `page.keyboard.type()` or `page.fill()`** to set editor content.
  Monaco's synthetic event model causes auto-indent stacking (a `:` at line-end
  triggers an extra indent level on top of the indentation you type) and some
  characters are swallowed by Monaco's suggestion engine. The result is silently
  garbled code.
- **Use `executeEdits` via `page.evaluate()`** for all programmatic content replacement:
  ```typescript
  await page.evaluate((code: string) => {
      const win = window as any;
      if (win.monaco?.editor) {
          const editors = win.monaco.editor.getEditors();
          if (editors.length > 0) {
              const model = editors[0].getModel();
              if (model) {
                  editors[0].executeEdits('e2e-replace', [{
                      range: model.getFullModelRange(),
                      text: code,
                  }]);
              }
          }
      }
  }, newCode);
  ```
- `executeEdits` preserves undo history and reliably fires `onDidChangeModelContent`
  → React `onChange`. `model.setValue()` also works but resets the undo stack and
  should be avoided unless you specifically need a full model reset.

---

## E2E Test Coverage

One Playwright test per active world. Run with:
```
npx playwright test tests/e2e/test_foundry_quest.spec.ts tests/e2e/test_world_*.spec.ts --headed
```

| Test file | World | Quest | Runner |
|---|---|---|---|
| `test_foundry_quest.spec.ts` | world-python (foundry) | hello-variable | Python local |
| `test_world_python_selenium.spec.ts` | world-python (selenium) | selenium-open-page | Chromium headless |
| `test_world_web_html.spec.ts` | world-web (html) | html-ignition | Node.js --test |
| `test_world_web_css.spec.ts` | world-web (css) | css-ignition | Node.js --test |
| `test_world_sql.spec.ts` | world-sql | sql-ignition | Postgres |
| `test_world_js.spec.ts` | world-js | js-ignition-q1-console-and-functions | Node local |
| `test_world_ts.spec.ts` | world-ts | ts-ignition | Bun |
| `test_world_git.spec.ts` | world-git | git-ignition | Shell local |

All 8 run in parallel in ~20s with no cross-test interference.

**Monaco editor rule:** Never use `page.keyboard.type()` or `page.fill()` for the code
editor. Use `window.monaco.editor.getEditors()[0].executeEdits()` via `page.evaluate()`.
See `test_foundry_quest.spec.ts` for the canonical reference pattern.

**Bugs fixed during e2e authoring (do not revert):**
- `QuestIDE.handleSubmit`: uses `conventionEntrypoint` for primary code resolution
  (same lookup as `handleRun`) — prevents empty code payloads for multi-file quests (JS/TS/Git)
- `quest_validate.py`: short-circuits placeholder guard for rule-free objective kinds (HTML/CSS)
- `code_runner.py`: `run_web_local()` runner for Node.js grading tests

---

## Common Scripts

| Script | Purpose |
|--------|---------|
| `scripts/dev-up.ps1` | Start full Docker stack |
| `scripts/dev-api.ps1` | Start backend with hot-reload |
| `scripts/questpack_seed.py` | **Canonical seeder** for `data/questpacks/*.json` files |
| `scripts/seed_evalforge_universe.py` | Seed legacy `docs/*.json` track specs only |
| `scripts/seed_bosses.py` | Seed boss definitions |
| `scripts/ingest_codex.py` | Index codex docs into pgvector |
| `scripts/init_local_db.py` | Initialize local DB schema |
| `scripts/audit_codex_refs.py` | Audit broken codex key-term references |
| `scripts/debt_breakdown.py` | Report on curriculum tech debt |
| `scripts/smoke_quest_api.py` | Full learner-path smoke test (all worlds) |
| `scripts/ci_check_modern_worlds.py` | CI regression guard (must pass before commit) |

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
