# Platform Architecture Audit
## Date: 2026-05-24
## Status: WALKTHROUGH FINDINGS UNRESOLVED

---

## Executive Summary

EvalForge today is a quest-execution platform with a working backend skeleton
(FastAPI + Postgres + Docker runners) and a frontend with **four UI layouts**
where only one (Workshop) is actively maintained. The CI gate is green, e2e
passes, and the training-grade snapshot matches — yet the manual walkthrough
exposed eight learner-facing grading bugs that the CI infrastructure
cannot detect because **it validates itself, not the learner experience**.

**What works:** the backend route handlers, the Docker runners, the workspace
hydration pipeline, the boss fight flow (Sprint 19), the questpack seeder,
and the test infrastructure. The Workshop layout's IDE is functional.

**What's broken in user-visible ways:** the grading pipeline lies on edge
cases. Specifically, `passed` defaults to `True` when no objectives are
evaluated — the "Optimistic for playground" branch at `routes_quests_runtime.py:371`.
This single line causes findings 2, 3, and 8 from the walkthrough. The frontend
entrypoint convention map (`QuestIDE.tsx:267-281`) defaults to `main.py` for
non-Python worlds, causing findings 1, 5, and 6. The `ready_to_submit` and
`passed` flags use different default logic (finding 7). The SQL preview
runner dispatches without a language guard (finding 4).

**Recommended path to usability:** four sprints. Sprint 21 fixes the grading
pipeline (the platform can't be used while grading lies). Sprint 22
consolidates to the Workshop layout. Sprint 23 fixes the language convention
maps. Sprint 24 deletes confirmed dead code.

### RECOMMENDED IMMEDIATE FIX (single-line, do not apply this sprint)

`arcade_app/routers/routes_quests_runtime.py:371` — change `passed = True`
to `passed = False`. The "Optimistic for playground" branch causes grading
to falsely report success when objective evaluation produces no results
(grader crashed, language mismatch, etc.). Fail-closed is the correct
default. This one change resolves three of the eight walkthrough findings.
Do not apply in this audit sprint — Sprint 21 will fix it with proper
context and tests.

---

## Section 1 — Grading Pipeline

### 1.1 End-to-End Trace: `python-dicts-lists-transform` Submission

| # | Step | File | Function | Lines |
|---|------|------|----------|-------|
| 1 | Run button click | `apps/web/src/components/quests/QuestIDE.tsx` | `handleRun()` | 644–714 |
| 2 | Payload construction | same | `handleRun()` | 675 (`mode="tests"` for tests_pass) |
| 3 | Backend route | `arcade_app/routers/routes_quests_runtime.py` | `run_quest()` | 82 |
| 4 | Quest resolution | same | `run_quest()` | 115 (slug lookup), 156 (language) |
| 5 | Workspace hydration | `arcade_app/services/utils.py` | `build_effective_workspace()` | 4–73 |
| 6 | Dispatch decision | `arcade_app/services/code_runner.py` | `run_code()` | 839, 871 (`use_docker` calc) |
| 7 | Runner entry resolution | `arcade_app/services/code_runner_docker.py` | `run_code_docker()` | 32–253 |
| 8 | Test runner copy-in | same | same | 122–132 (copies `run_unittest_json.py` → `.evalforge/`) |
| 9 | Pytest invocation | `arcade_app/services/runner_registry.py` | `get_runner()` | 19–26 (`["python", "-u", "-I", "-B", "/workspace/.evalforge/run_unittest_json.py"]`) |
| 10 | Pytest run | `arcade_app/services/run_unittest_json.py` | (main) | 30–104 |
| 11 | Result post-processing | `arcade_app/routers/routes_quests_runtime.py` | `run_quest()` | 345 (`validate_quest_attempt`), 363–371 (`passed` calc), 633 (`ready_to_submit`) |
| 12 | Response shape | same | same | 644 (`evaluated_objectives` set from payload) |
| 13 | Frontend response handling | `apps/web/src/components/quests/QuestIDE.tsx` | `handleRun()` success branch | 706–841 |
| 14 | Success overlay | `apps/web/src/components/quests/QuestSuccessOverlay.tsx` | `QuestSuccessOverlay` | 13–75 |

### 1.2 Root Cause for Each Walkthrough Finding

| # | Finding | File:Line | Current Behavior | Why Wrong |
|---|---------|-----------|------------------|-----------|
| 1 | main.py / example.py contradiction | `QuestIDE.tsx:267-281` | `conventionEntrypoint` hardcoded by language; falls back to `filesToLoad[0]` when convention file not found | For non-canonical Python quests, alphabetical-first file (e.g., `example.py`) gets opened even though convention chip says `main.py` |
| 2 | "run_unittest_json.py not found" but passed:true | `code_runner_docker.py:125-132` (copy-in) + `routes_quests_runtime.py:371` (`passed = True`) | Runner IS copied correctly into container, but if language ≠ python/sql the test mode produces no objective_results, then the optimistic branch sets `passed=True` | The "not found" symptom is misleading — the actual bug is that **non-Python quests should never enter test mode at all** (language guard missing) AND when grading produces nothing, `passed=True` is the wrong default |
| 3 | first-sparks: `evaluated_objectives:false` but `passed:true` | `routes_quests_runtime.py:312-317` | When `evaluate_objectives=False`, code sets `objective_results=[]` AND `passed=True` | The two flags are independent; `passed` should not be true when objectives weren't evaluated. They are semantically incompatible |
| 4 | SQL preview attaches to non-SQL quests | `routes_quests_runtime.py:249` ("sql_preview" string), `code_runner.py:871` (dispatch) | `runner_id = "sql_preview" if lang == "sql" and exec_mode == "run" else None`. The guard exists for `runner_id` but the actual dispatch in `code_runner.py` lacks a corresponding check | The runner_id assignment guards on language but `run_code_docker` then dispatches based on its own logic; there's no single source of truth |
| 5 | Entrypoint chip falls back to "main.py" for non-python | `QuestIDE.tsx:267-276` | Switch only covers sql, typescript, javascript, css, html, shell, playwright. Default branch returns `'main.py'` | Worlds `git`, `docker`, `agents`, `node` have no entry and fall to Python default |
| 6 | Initial active file is alphabetical for non-python | `QuestIDE.tsx:279` | When convention file not in filesToLoad, falls back to `filesToLoad[0].path`. Files arrive sorted alphabetically from backend (`utils.py:64`) | For a CSS quest with `example.css` and `style.css`, opens `example.css` first |
| 7 | `ready_to_submit` and `passed` disagree | `routes_quests_runtime.py:363-371` vs `:633` | `passed = True` if objective_results empty (line 371). `ready_to_submit = (passed and not timed_out) if evaluate_objectives else False` (line 633). Different default logic for the same condition | When `evaluate_objectives=True` but `objective_results=[]`, `passed=True` but `ready_to_submit=True` (since both `passed` and `not timed_out`) — actually agrees here. The disagreement appears when `evaluate_objectives=False` → `passed=True`, `ready_to_submit=False` |
| 8 | "Mission Accomplished" when grader crashed | `QuestSuccessOverlay.tsx:51` | Generic fallback message when no `debrief` data | Triggered by `result.passed=true` from frontend, which came from the optimistic branch in finding #2. Symptom of finding #2 |

**Three findings (2, 3, 8) trace to the same root cause:** `routes_quests_runtime.py:371` defaults `passed` to `True` on empty `objective_results`. Fix-closed (line 371: `passed = False`) resolves all three.

**Two findings (5, 6) trace to the same root cause:** `QuestIDE.tsx:267-281` convention map is incomplete for non-Python worlds AND falls back to alphabetical-first file.

**Finding 4 is a language-guard inconsistency** between `runner_id` resolution in `routes_quests_runtime.py` and actual dispatch in `code_runner.py`.

### 1.3 Runner Inventory

| Runner | File:Line | Languages | Status | Dispatched By | Has Language Guard | Populates objective_results |
|--------|-----------|-----------|--------|---------------|--------------------|----------------------------|
| `run_python_local()` | `code_runner.py:23` | python | ACTIVE | fallback in `run_code()` for dev | No | No (validation post-run) |
| `run_javascript_local()` | `code_runner.py:322` | javascript | ACTIVE | fallback in `run_code()` for dev | No | No |
| `run_shell_local()` | `code_runner.py:458` | shell | ACTIVE | `run_code():856` | **Yes** (`if language == "shell"`) | No |
| `run_web_local()` | `code_runner.py:533` | html, css | ACTIVE | `run_code():862` | **Yes** (`if language in ("html","css")`) | **Yes** (parses Node test output) |
| `run_playwright_local()` | `code_runner.py:685` | playwright | ACTIVE | `run_code():` | **Yes** (`if language == "playwright"`) | **Yes** (exit code) |
| `run_docker_local()` | `code_runner.py:815` | docker | ACTIVE | `run_code():852` | **Yes** (`if language == "docker"`) | No (grade-by-inspection — handled by `yaml_structure` objectives) |
| `run_code_docker()` | `code_runner_docker.py:32` | all (esp. python+sql tests) | ACTIVE | `run_code():876` when `use_docker` true | No | Indirect (via post-run `validate_quest_attempt`) |
| `run_code()` (dispatcher) | `code_runner.py:839` | all | ACTIVE | route handler entry | Partial — guards exist for shell, html/css, playwright, docker but not for python/javascript/sql/typescript | N/A |

**Findings:**
- All 7 runners are USED. No DEAD runners.
- **4 runners have explicit language guards** (shell, html/css, playwright, docker). These are the new-world worlds added in recent sprints — the guards reflect the lessons learned.
- **The older runners (python_local, javascript_local, code_runner_docker) have no early language guards**. They rely on dispatcher arithmetic in `run_code():871` (`use_docker = ... or (language not in ["python","javascript"]) or (mode == "tests")`). When that arithmetic produces an unexpected result (e.g., a git quest with `mode="tests"` gets sent to docker runner), there is no defensive language check.
- **The SQL preview runner (`sql_preview`) is dispatched by `runner_id` string in the route handler**, but the actual runner spec lookup is in `runner_registry.py`. The route handler's guard (`if lang == "sql" and exec_mode == "run"`) is correct, but it's structurally separate from the dispatcher in `code_runner.py`, so any future change in either place can desync them.
- **Objective evaluation is centralized in the route handler** (`routes_quests_runtime.py:345`), not in the runners. This is good architecturally (single source of truth) but means runners can silently return "no output" and the validator will produce empty `objective_results` — which then triggers the `passed=True` optimistic branch.

---

## Section 2 — UI Layouts

### 2.1 Layout Inventory

| Layout | File | Routes | Last Update | Status |
|--------|------|--------|-------------|--------|
| **Workshop** | `apps/web/src/layouts/WorkshopLayout.tsx` | `/arcade/workshop`, `/arcade/workshop/quests/:questId`, `/arcade/worlds/:worldSlug/quests/:questId`, `/arcade/worlds/:worldSlug/bosses/:bossSlug`, `/arcade/projects/:projectSlug/*` | 2026-05-21 (3 days ago) | **ACTIVE — keeper** |
| **Orion** | `apps/web/src/layouts/OrionLayout.tsx` | `/arcade/orion`, `/arcade/worlds/:worldSlug` | 2026-01-15 (~4 months) | STALE — visible in header switcher; world-map view only |
| **Cyberdeck** | `apps/web/src/layouts/CyberdeckLayout.tsx` | `/arcade/deck` | 2025-12-05 (~5 months) | ABANDONED — retro aesthetic shell, no functional integration with current quest IDE |
| **GameShell** | `apps/web/src/layouts/GameShell.tsx` | wraps all `/arcade/*` | — | Wrapper only — delegates to DevUI; not a layout in the user-facing sense |

### 2.2 Feature Matrix

| Feature | Workshop | Orion | Cyberdeck | Notes |
|---------|----------|-------|-----------|-------|
| Quest IDE (Monaco + run + submit + result panel) | ✓ | — | ◯ | Cyberdeck receives a `questPanel` prop but no modern IDE wiring |
| Quest list / world selection | ✓ | ✓ | ◯ | Orion has interactive star-map; Workshop has QuestBoard |
| Briefing / tutorial / hints | ✓ | — | — | Workshop only |
| Boss fight UI | ✓ | ◯ | — | Orion shows `RightRailBossPracticeColumn` as a preview side panel |
| Codex search / drawer | ✓ | — | — | Workshop only |
| Settings / preferences | ✓ | ✓ | ✓ | Global `GameShellHeader` handles this |
| Progress / XP / level | ✓ | ◯ | — | Orion has `ActiveTrackStatus` footer |
| Practice gauntlet card | ✓ | ◯ | ◯ | Workshop only meaningful integration |
| Auth / login | ✓ | ✓ | ✓ | Global DevUI handles this |
| HUD elements (EventLog, NetworkPanel) | ◯ | ✓ | ◯ | Network panel is decorative-only in Cyberdeck |

Legend: ✓ present and current · ◯ present but stale or incomplete · — not present

### 2.3 Consolidation Recommendation

**Keep Workshop. Drop Orion and Cyberdeck as top-level layouts.**

| Action | What | Effort |
|--------|------|--------|
| Keep `WorkshopLayout` | Most complete, most recent, default route, has IDE + boss + codex + tools | — |
| Delete `CyberdeckLayout.tsx` | 5+ months stale, no unique features. Routes (`/arcade/deck`) can 301-redirect to `/arcade/workshop`. CRT-mode toggle in `settingsStore` becomes unused (delete it too) | **S** (≤2h) |
| Drop `OrionLayout.tsx` as a layout, keep `OrionMap` component | OrionMap is already rendered inside Workshop's list view. The layout wrapper itself is the only thing dropped. RightRailBossPracticeColumn can either migrate to a Workshop drawer or be deleted | **S** (≤4h) |
| Remove Orion/Cyberdeck buttons from `GameShellHeader` layout switcher | The switcher itself can go too if there's only one layout | **S** (≤1h) |
| Audit `useGameStore.layout` field | Currently tracks which of three layouts is active. Becomes dead after consolidation | **S** (≤1h) |

**Total: ~8 hours to single-layout state.**

---

## Section 3 — Debt Catalog

### 3.1 Routers

| Router | Status | Notes |
|--------|--------|-------|
| `avatars.py`, `routes_boss.py`, `routes_boss_codex.py`, `routes_boss_runs.py`, `routes_coach.py`, `routes_codex.py`, `routes_db.py`, `routes_ladders.py`, `routes_practice_rounds.py`, `routes_profile.py`, `routes_qa.py`, `routes_quests.py`, `routes_tools.py`, `routes_universe.py`, `routes_workshop.py`, `routes_world_progress.py`, `session.py`, `skills.py`, `projects.py`, `project_codex.py`, `intent_oracle_eval.py` | ACTIVE | Registered AND used by frontend |
| `routes_quests_runtime.py` | **DUPLICATE** — uses same `/api/quests` prefix as `routes_quests.py` and defines overlapping endpoints (both have POST `/submit`) | Both routers registered. The route handlers do different things but the URL space collides. FastAPI takes whichever was included first. This is fragile |
| `auth.py` | **UNREGISTERED** — file has `# STATUS: unregistered` header. Auth logic lives in `auth_helper.py` dependencies instead | Decision needed: delete or activate |
| `reporting.py` (`GET /dev/grades/export`) | **UNUSED** — no frontend caller, dev-only markdown/JSONL export | Delete candidate |

### 3.2 Scripts

The agent counted **200+ Python scripts** in `scripts/`. Cleanup is overdue.

**ACTIVE (~30 scripts)** — referenced by CI, CLAUDE.md, dev-up, or docker-compose:
- Audits: `audit_skipped_tests.py`, `audit_codex_consistency.py`, `audit_codex_quality.py`, `audit_quest_content.py`, `audit_quest_panels.py`, `audit_all_worlds.py`, `audit_questpack_hydration.py`
- CI: `ci_check.py`, `ci_check_modern_worlds.py`, `certify_training_grade.py`, `verify_all_modern_worlds.py`
- Seeders: `seed_all.py`, `seed_bosses.py`, `seed_evalforge_universe.py`, `questpack_seed.py`, `init_local_db.py`
- Validators: `curriculum_validator.py`, `validate_tutorials.py`, `runner_preflight.py`
- Misc: `mock_cms_app.py` (docker-compose), `smoke_quest_api.py`, `check_cherry_pick_diff.py`, `ingest_codex.py`, `dev-up.ps1`, `dev-api.ps1`, `install-hooks.ps1`

**ONE-OFF (likely completed migrations) — DELETE CANDIDATES (~15 scripts):**
- `backfill_objectives_missing.py`, `backfill_quest_panels.py`, `backfill_tier1_docs.py`
- `capture_golden_batch.py`, `capture_golden_state.py`, `capture_golden_stdout.py`, `capture_golden_via_unified_runner.py`
- `cleanup_orphans.py`
- `example_zero_boss_judge.py`
- `legacy_quest_audit.py`, `modernize_wrappers.py`, `optimize_codex_refs.py`
- `force_seed_standard.py`, `sync_seed_standard.py`
- `regenerate_snapshot.py`, `regenerate_tutorials.py`
- `tutorial_backfill_suggest.py`, `world_backfill_tutorials.py`

**SCAFFOLDING (~30 scripts)** — content generation utilities, low priority:
- `scaffold_*.py` family — generators for new world/quest content
- `generate_*.py` family — content generation helpers
- `upgrade_*.py` family — old upgrade scripts

**DEBUG / DIAGNOSTIC (~50+ scripts)** — should be moved to `scripts/debug/`:
- `check_*.py`, `debug_*.py`, `dump_*.py`, `extract_*.py`, `inspect_*.py`, `test_*.py`, `verify_*.py` (NOTE: some `verify_*.py` are in CI — distinguish carefully)

**UNCLEAR (~30 scripts)** — need owner review:
- `categorize_coverage_buckets.py`, `currency_population_audit.py`, `dev_validate_all.py`, `diag_quest_content.py`, `extract_quest_signals.py`, `force_seed_standard.py`, `gather_web_context.py`, `hydrate_agents_from_docs.py`, `ingest_rubrics.py`, `manual_sync.py`, `mock_boss_judge.py`, `mock_boss_judge_curator.py`, `mock_prism_judge.py`, `plan_golden_rollout.py`, `quest_new.py`, `quest_preview.py`, `ratchet_golden_budget.py`, `register_subagent.py`, `repro_codex_fetch.py`, `reset_*.py`, `sql_wave_guardrail.py`, `utils_questpacks.py`

### 3.3 Database Tables

| Table | Status | Notes |
|-------|--------|-------|
| `User`, `Profile`, `AvatarDefinition`, `UserSkill`, `Project`, `ProjectCodexDoc`, `KnowledgeChunk`, `BossDefinition`, `BossRun`, `BossProgress`, `BossCodexProgress`, `TrackDefinition`, `QuestDefinition`, `QuestProgress`, `QaRun`, `QaBatchRun` | ACTIVE | Read AND written by current code |
| `SkillNode` | READ-ONLY | Static reference data; seeded once |
| `UserMetric` | READ-ONLY (light) | Only 1 read site; verify intent |
| `BadgeDefinition` | **VESTIGIAL** | 0 reads, 1 write. Abandoned badging feature |
| `UserBadge` | UNCLEAR | Paired with abandoned BadgeDefinition |
| `ChatSession` | UNCLEAR | Only 1 read site; likely legacy |

`QuestDefinition` is the most-read table (21 select call sites). Worth ensuring the `(world_id, track_id, slug)` index exists if not already.

### 3.4 Data Directory Orphans

**152 quest directories in `data/quests/` have no entry in any active questpack.** This is ~60% of all quest workspaces on disk. Most are not currently visible to the learner. They include:
- The entire `agents-*` family (Sprint 1 work on world-agents that was never finished)
- Foundational quests replaced by newer versions: `first-sparks`, `git-add-commit`, `git-branches`, `git-ignition`, `git-init-clone`, `git-log`, etc.
- A `_shared` directory of shared assets (not a quest, but lives in this tree)

**46 questpack entries reference workspace directories that do NOT exist on disk.** Examples from the agent's scan:
```
cli_core.json:        cli-pipes          → ../quests/cli-pipes/workspace [MISSING]
cli_core.json:        cli-env-vars       → ../quests/cli-env-vars/workspace [MISSING]
docker_ignition.json: dk-hello-container → ../quests/dk-hello-container/workspace [MISSING]
docker_systems.json:  dk-compose-basics  → ../quests/dk-compose-basics/workspace [MISSING]
node_core.json:       node-ignition      → ../quests/node-ignition/workspace [MISSING]
playwright_ignition.json: pw-record-and-run → ../quests/pw-record-and-run/workspace [MISSING]
python_ignition.json: py-ignition-variables → ../quests/py-ignition-variables/workspace [MISSING]
```

**This is the biggest data-integrity issue surfaced by the audit.** The
`audit_questpack_hydration.py` script (Sprint 18) catches missing entrypoints
in seeded DB rows but **does not catch questpack entries whose `files_from`
directory is missing entirely**. The seeder silently creates an empty
workspace_json `{"files": []}` for these. The DB validation passes (it
checks the seeded row), but the quest will not work for a learner.

**0 audit files older than 60 days.** Good — Sprint 15 cleanup held.

### 3.5 Frontend State Slices

| Store | File | Status |
|-------|------|--------|
| `useQuestStore` | `store/questStore.ts` | ACTIVE |
| `useGameStore` | `store/gameStore.ts` | ACTIVE (but `layout` field becomes dead after consolidation in Section 2) |
| `useBossStore` | `store/bossStore.ts` | ACTIVE |
| `useSettingsStore` | `store/settingsStore.ts` | ACTIVE (but `crtMode` field becomes dead after Cyberdeck delete) |
| `useAgentStore` | `store/agentStore.ts` | ACTIVE |
| `useCurriculumStore` | `store/curriculumStore.ts` | **UNUSED** — 0 references in apps/web/src/. Contains mock data only. Delete candidate |

---

## Section 4 — Inconsistencies

### 4.1 Magic Paths

| Pattern | Files | Notes |
|---------|-------|-------|
| `.evalforge/` (artifacts dir) | `code_runner_docker.py:123, 176, 204, 264`, `runner_registry.py:25, 39` | Backend only; consistent |
| `/workspace` (Docker container path) | `code_runner_docker.py:182, 186, 283, 288`, `run_unittest_json.py:17`, `security.py` | Backend only; consistent |
| `data/quests/` | `code_runner.py:42-48`, `code_runner_docker.py:70`, `routes_quests_runtime.py:139, 209`, `seed_quests_standard_worlds.py` | **Mix of relative and absolute paths**, some Windows-specific (`d:\EvalForge\data\quests\…`) |
| `data/questpacks/` | various seeders | No hardcoded paths; loaded via configured list |
| `/app/` (legacy container path) | `code_runner.py:42` (fallback only) | Deprecated; can be removed |
| `run_unittest_json` | `services/run_unittest_json.py` (source), `runner_registry.py:25, 39` (invoked path) | **NOT a path mismatch.** Source is copied into container's `.evalforge/` at runtime by `code_runner_docker.py:125-132`. The walkthrough's "not found" symptom must come from a different path — most likely a non-Python quest entering test mode (see finding #2) |

### 4.2 Language Convention Maps

**Six separate maps in the codebase, all with different missing entries.** This is the single most consequential pattern in the audit — it underlies findings 1, 2, 5, and 6.

| Map | File:Line | Active worlds it covers | Worlds missing | Fallback |
|-----|-----------|------------------------|----------------|----------|
| Frontend entrypoint convention | `QuestIDE.tsx:267-276` | sql, typescript, javascript, css, html, shell, playwright, python | docker, git, agents, node, web | `main.py` |
| Backend Docker runner entrypoint | `code_runner_docker.py:43-59` | sql, typescript | python (via workspace fallback), everything else default to `main.py` | `main.py` |
| Backend effective execution entrypoint | `code_runner_docker.py:155-170` | sql, typescript, javascript, python | shell, docker, git, playwright, css, html, web, agents | None / falls through |
| Local run convention (Python-assumed) | `code_runner.py:102-138` | python | All others; treats everything as Python | `task.py` → `main.py` |
| Coach prompts language map | `coach_prompts.py:53` | sql | All others | Not specified |
| Quest helper file extension | `quest_helper.py:331-338` | sql, javascript, typescript, html, css, python | shell, docker, git, playwright, web, agents | `main.py` |

**Critical observation:** the active worlds documented in `CLAUDE.md` and
`configs/curriculum_guardrail_scope.json` include `world-python`, `world-web`,
`world-sql`, `world-js`, `world-ts`, `world-git`, `world-docker` —
**but no single map in the codebase covers all of them.** Every map is
incomplete for at least one active world. The walkthrough's "main.py
fallback for non-Python worlds" is the user-visible manifestation of this
gap.

### 4.3 Status Flag Semantics

| Flag | Set At | Meaning Per Code | Default |
|------|--------|------------------|---------|
| `passed` | `routes_quests_runtime.py:363-371` | `True` if all `objective_results` are `ok`, OR if `objective_results` is empty AND mode≠"execute" | `True` on empty objectives ("Optimistic for playground" comment at line 371) |
| `objective_results` | `routes_quests_runtime.py:345` (from `validate_quest_attempt`) | List of objective dicts: `[{"id","ok","detail"}]`. Empty = preview run OR no rules defined OR grader produced no output | `[]` |
| `evaluated_objectives` | `routes_quests_runtime.py:312, 644` | Boolean from payload. `True` = run was a grading run; `False` = preview/reference run | `True` (schema default) |
| `ready_to_submit` | `routes_quests_runtime.py:633` | `(passed and not timed_out) if evaluate_objectives else False` | `False` in preview mode; depends on `passed` otherwise |

**Should they agree?** In principle:
- `evaluated_objectives=False` ⇒ `passed=neutral` and `ready_to_submit=False`. Today: `passed=True` (wrong; it's not graded).
- `evaluated_objectives=True` AND `objective_results=[]` ⇒ ambiguous. Today: `passed=True` (optimistic). Should be: `passed=False` (fail-closed, since either grader crashed or quest has no rules).
- `evaluated_objectives=True` AND `objective_results` populated ⇒ `passed = all ok`. Today: correct.

**The four-flag system is fundamentally salvageable** — the semantics are
clear and the conditions are unambiguous. The bug is that `passed`'s
default value contradicts its semantic meaning. A one-line fix at
`routes_quests_runtime.py:371` (`passed = True` → `passed = False`)
realigns the system.

**Frontend reads:** the success overlay checks `result.passed` (boolean),
not `result.ready_to_submit`. This means the "Mission Accomplished" path
is driven by `passed`, not by the more conservative `ready_to_submit`.
This is consistent with the bug: the optimistic `passed=True` triggers
the overlay even when nothing was actually graded.

---

## Section 5 — Recommended Sprint Sequence

### Sprint 21 — Grading pipeline correctness (FIRST PRIORITY)

**Goal:** make `passed`, `objective_results`, `evaluated_objectives`, and `ready_to_submit` agree across every quest type.

**Scope:**
- `arcade_app/routers/routes_quests_runtime.py:312-371, 633, 644` — flag computation
- `arcade_app/services/quest_validate.py` — ensure validators always return at least one result row (config_missing rather than empty list)
- `apps/web/src/components/quests/QuestSuccessOverlay.tsx:51` — don't celebrate on empty objective_results
- `apps/web/src/components/quests/QuestIDE.tsx` — frontend should treat `result.passed && objective_results.length>0` as the success condition, not just `result.passed`
- Test additions: backend test that runs each of the 8 walkthrough scenarios end-to-end

**Out of scope:** new runners, new content, layout changes, language map unification (Sprint 23 territory).

**Acceptance criteria:**
1. Submitting broken code to a tests_pass quest returns `passed=false` and shows the failure in UI.
2. Submitting code to a quest with NO objectives defined returns `passed=false` with a clear `config_missing` objective failure.
3. Preview mode (`evaluate_objectives=false`) returns `passed=null` or `passed=false` (NOT true), and the UI does not show success overlay.
4. All 8 walkthrough findings either resolve OR have a tracked deferred-fix ticket (with explanation of why deferred).
5. New test file `tests/backend/test_grading_truth_table.py` exists and covers each `(evaluated_objectives × objective_results) ∈ {true,false} × {empty,populated}` cell.

**Estimated effort:** 1–2 days.

---

### Sprint 22 — UI layout consolidation

**Goal:** collapse to a single Workshop layout.

**Scope:**
- Delete `apps/web/src/layouts/CyberdeckLayout.tsx` and its route
- Demote `OrionLayout` to a Workshop view-mode (keep `OrionMap` component, drop the layout wrapper)
- Remove `useSettingsStore.crtMode` field (Cyberdeck-only)
- Remove `useGameStore.layout` field (only one layout)
- Remove `useCurriculumStore` entirely (unused — Section 3.5)
- Update `GameShellHeader` layout switcher (delete or reduce to single button → no switcher)
- Migrate `RightRailBossPracticeColumn` to a Workshop drawer if any feature still needs it; otherwise delete
- Update e2e tests that reference Orion/Cyberdeck

**Out of scope:** Workshop polish, new features, new layouts.

**Acceptance criteria:**
1. All routes outside `/arcade/workshop` redirect (or are deleted)
2. No references to Orion/Cyberdeck remain in the codebase
3. e2e suite still passes
4. Manual walkthrough confirms learner sees consistent UI everywhere

**Estimated effort:** 1 day.

---

### Sprint 23 — Language convention unification

**Goal:** replace six scattered language maps with a single source of truth.

**Scope:**
- Create `arcade_app/services/language_config.py` (or `apps/web/src/config/languageConfig.ts`) — a single dict keyed by language, with fields: `entrypoint`, `extension`, `runner`, `supports_tests`, `display_name`, `test_runner_path`
- Both backend and frontend import from this canonical map (shared via codegen or a JSON file in `configs/`)
- Replace the six maps identified in Section 4.2 with lookups into the canonical map
- Add an audit script `scripts/audit_language_coverage.py` that fails CI if any active world has no entry in the canonical map

**Out of scope:** runner refactoring; content changes; new languages.

**Acceptance criteria:**
1. Single language config file exists with entries for all active worlds (python, web/html, web/css, sql, js, ts, git, docker)
2. Every place that previously had a language switch now reads from the canonical map
3. CI audit verifies completeness — adding a new world without updating the map fails CI
4. Walkthrough finding #5 (entrypoint chip wrong for non-python) is resolved

**Estimated effort:** 1 day.

---

### Sprint 24 — Cleanup (confident dead code only)

**Goal:** delete confirmed-dead code with no functional impact.

**Scope (see Section 6 for the complete delete list):**
- 1 router (`reporting.py`)
- 1 DB table (`BadgeDefinition`) + migration to drop column refs
- 1 frontend store (`useCurriculumStore`)
- ~15 one-off scripts (the `backfill_*`, `capture_golden_*`, `cleanup_*`, `regenerate_*`, `force_seed_*` family)
- 1 layout (`CyberdeckLayout.tsx`) — already done in Sprint 22

**Out of scope:** "UNCLEAR" tables and scripts (need owner review first); duplicate routers (need a deeper consolidation sprint).

**Acceptance criteria:**
1. Every item in Section 6 is either deleted OR marked NOT-DELETE with a one-line reason in this audit
2. CI still passes
3. e2e still passes
4. `git log --diff-filter=D --name-only -1` shows only the items in Section 6

**Estimated effort:** ½ day.

---

### Sprint 25 (optional, follow-up) — Data integrity

**Goal:** resolve the 152 orphan workspaces and 46 broken questpack references.

**Scope:**
- Extend `audit_questpack_hydration.py` to also flag missing `files_from` directories (currently only checks DB row hydration)
- Decide per-orphan: keep (link into a questpack), archive (move to `data/quests/_archive/`), or delete
- Fix or remove the 46 broken questpack references

**Estimated effort:** 1 day (mostly review).

---

## Section 6 — What to Delete

Confidently dead, safe to delete in a cleanup sprint:

### Files

| Path | Why dead | Confidence |
|------|----------|------------|
| `apps/web/src/store/curriculumStore.ts` | 0 references in apps/web/src/; contains mock data only | High |
| `apps/web/src/layouts/CyberdeckLayout.tsx` | 5+ months stale; no unique features; agent could not find functional integration with current IDE | High |
| `arcade_app/routers/reporting.py` (GET /dev/grades/export) | No frontend caller; dev-only endpoint | High |

### Database

| Table | Why dead | Confidence |
|-------|----------|------------|
| `BadgeDefinition` | 0 reads across entire codebase; 1 write (seed); paired with abandoned UserBadge | High (verify with `grep BadgeDefinition arcade_app/` before delete) |

### One-off scripts (likely completed migrations)

| Path | Why dead | Confidence |
|------|----------|------------|
| `scripts/backfill_objectives_missing.py` | Backfill (completed) | Medium |
| `scripts/backfill_quest_panels.py` | Backfill (completed) | Medium |
| `scripts/backfill_tier1_docs.py` | Backfill (completed) | Medium |
| `scripts/capture_golden_batch.py` | One-time snapshot capture | Medium |
| `scripts/capture_golden_state.py` | One-time snapshot capture | Medium |
| `scripts/capture_golden_stdout.py` | One-time snapshot capture | Medium |
| `scripts/capture_golden_via_unified_runner.py` | One-time snapshot capture | Medium |
| `scripts/cleanup_orphans.py` | One-time cleanup | Medium |
| `scripts/example_zero_boss_judge.py` | Example/demo code | High |
| `scripts/legacy_quest_audit.py` | Legacy migration audit | Medium |
| `scripts/modernize_wrappers.py` | One-time modernization | Medium |
| `scripts/optimize_codex_refs.py` | One-time optimization | Medium |
| `scripts/regenerate_snapshot.py` | One-time regeneration | Medium |
| `scripts/regenerate_tutorials.py` | One-time regeneration | Medium |
| `scripts/tutorial_backfill_suggest.py` | One-time backfill | Medium |
| `scripts/world_backfill_tutorials.py` | One-time backfill | Medium |
| `scripts/sync_seed_standard.py` | Likely one-time sync (verify before delete) | Medium |
| `scripts/force_seed_standard.py` | Likely one-time force-seed (verify before delete) | Medium |

### Frontend state fields (deletable after Sprint 22)

| Field | File | Why dead | Confidence |
|-------|------|----------|------------|
| `useSettingsStore.crtMode` | `store/settingsStore.ts` | Only used by Cyberdeck layout (Section 2 drops it) | High (after Sprint 22) |
| `useGameStore.layout` | `store/gameStore.ts` | Tracks active layout when there are three; becomes dead with single layout | High (after Sprint 22) |

### NOT in delete list (despite looking suspicious)

| Item | Why kept | Reason |
|------|----------|--------|
| `arcade_app/routers/auth.py` (UNREGISTERED) | Decision needed | Could be activated or removed; needs owner call |
| `routes_quests_runtime.py` / `routes_quests.py` (DUPLICATE) | Requires real refactor | Endpoints have different behaviors; consolidating is its own sprint |
| `ChatSession`, `UserMetric` tables (UNCLEAR) | Insufficient evidence | Might be used by analytics/admin paths not in main codebase |
| `agents-*` orphan quests (Sprint 1 work) | Decision needed | Could be reactivated as world-agents content; needs owner call |
| All `scaffold_*.py` scripts | Active content tools | Generators for new world/quest content; archive to `scripts/scaffold/` rather than delete |

---

**End of audit. No code changes were made in this sprint. The next sprint (Sprint 21) uses this document as input to scope grading-pipeline fixes.**

---

## Sprint 25 Backlog Note (added Sprint 24) — RESOLVED Sprint 28

### ~~Known Infrastructure Gap: DinD Path Resolution for `mode='tests'` Quests~~ RESOLVED

**Original symptom (now fixed):**
```
ERROR python: can't open file '.evalforge/run_unittest_json.py': [Errno 2] No such file or directory
ERROR [FAIL] tests_pass: No test output received
```

**Actual root cause (Sprint 28 diagnosis):** Two separate bugs, not a DinD path issue:

1. **`code_runner_docker.py` — conditional runner injection:** `run_unittest_json.py` was
   only copied into `.evalforge/` when `if code:` was True. Empty or missing `code`
   caused the runner container to start without the script → Python error. `sanitize_logs`
   then stripped `/workspace/` from the path, making it appear as `.evalforge/...` instead
   of `/workspace/.evalforge/...`.

2. **`routes_quests_runtime.py` — SUBMIT hardcoded `mode="run"`:** The `submit_quest`
   handler forced `mode="run"` regardless of quest type and never injected grading test
   files. All `tests_pass` objectives therefore received empty stdout and reported
   `"No test output received"` — even for the reference solution.

**Fix (Sprint 28):**
- `arcade_app/services/code_runner_docker.py`: Moved `run_unittest_json.py` injection
  outside of the `if code:` block. It now runs unconditionally for `mode="tests"`.
- `arcade_app/routers/routes_quests_runtime.py`: `submit_quest` now detects
  `tests_pass` objectives, sets `exec_mode = "tests"`, and injects grading test files
  from `grading/public/` — identical to the RUN endpoint's logic.

**Why the Sprint 24 diagnosis was wrong:** The error message said `.evalforge/run_unittest_json.py`
(relative path). The Sprint 24 investigator saw a relative path, noted that the registry spec uses
an absolute path (`/workspace/.evalforge/...`), and concluded that docker cp must be failing to
deliver the file — so the container was searching relative to its working directory. This pointed
at DinD path translation as the cause. What was missed: `sanitize_logs()` at `security.py:86`
strips `/(?:tmp|workspace)/+` from all learner-facing output. The path WAS absolute in the
container; the relative appearance was an artifact of log sanitization. The docker cp approach
works correctly on this platform.

**Environmental assumptions:** Requires Docker socket mounted into the backend container
(`//var/run/docker.sock:/var/run/docker.sock` in `docker-compose.yml`). The fix works
because `docker cp` runs inside the backend container (Linux), so temp-dir paths are
Linux paths resolvable by the Docker CLI. No Windows path translation needed.

**Process lesson — re-investigating "known issues":** This bug was labeled "known" and
"PENDING" for 4 sprints without re-investigation. The original hypothesis (DinD path
translation) was plausible but never verified by checking whether `docker cp` actually
failed. A 10-minute repro — `curl` to the RUN endpoint with empty code, then with the
reference solution — would have distinguished "file not delivered" from "endpoint logic
wrong" in Sprint 25. Long-standing "known issues" with confident-sounding root causes
deserve fresh eyes before each sprint that claims to address them. Hypothesis ≠ diagnosis.

**Verified (Sprint 28):**
- `python-file-io-safe` RUN (stub): `passed: false`, real test failures in `objective_results`
- `python-file-io-safe` SUBMIT (solution): `ok: true`, `status: completed`
- `python-file-io-safe` SUBMIT (stub): `ok: false`, real test failure names in `detail`
- `python-systems-resilient-job-runner` RUN (solution): `passed: true`, 6/6 tests
- `python-systems-resilient-job-runner` SUBMIT (solution): `ok: true`, `status: completed`
- `hello-variable` RUN (solution): `passed: true` — no regression in run-mode quests
- `selenium-open-page` RUN (stub): proper error response — no regression in Selenium quests

**Regression armor (Sprint 29):** `TestSubmitEndToEnd` class added to
`tests/backend/test_grading_truth_table.py` (4 tests, no Docker required):
- `test_submit_calls_run_code_with_mode_tests_for_tests_pass_quest` — bites when Bug 2 reintroduced
- `test_submit_stdout_regex_quest_uses_mode_run` — control: verifies non-tests_pass quests unaffected
- `test_submit_tests_pass_quest_returns_ok_false_on_failure` — verifies failure path shape
- `test_code_runner_docker_stages_runner_for_empty_code_in_tests_mode` — bites when Bug 1 reintroduced



---

## Backlog: Quest Drift Detection � Pairwise Audit Method (Sprint 26)

**Finding:** The three-way content mismatch in `python-systems-platform-tooling`
(docs described `slugify`/`unique_sorted`/`run_tool_request`; `task.py` described a
CLI greet/sum interface; `test_*.py` and `workspace/main.py` tested `parse_semver`)
escaped two separate content audits (Sprints 24 and 25).

**Root cause of audit gap:** Both audits compared docs against the grading test only.
Neither checked workspace files against each other. The CLI greet/sum description in
`task.py` and the `parse_semver` stub in `workspace/main.py` were invisible to a
docs-vs-test comparison.

**Recommended future audit method:** For each quest, run a three-way pairwise check:

1. `docs/briefing.md` vs. `grading/public/test_*.py` � does the briefing describe
   what the test checks?
2. `workspace/main.py` (or `task.py`) vs. `grading/public/test_*.py` � do the stubs
   expose the same names the test imports?
3. `workspace/task.py` vs. `workspace/main.py` � do both workspace files describe
   the same task?

Any mismatch in (2) is an immediate red flag: if the test contains
`from main import foo` but `workspace/main.py` defines `bar`, a learner filling in
the stub cannot pass the test regardless of how good the docs are.

**Worth adding to:** `scripts/certify_training_grade.py` as an automated
stub-vs-test import cross-check (low complexity: parse the `from main import ...`
line in each test, confirm each imported name appears as a `def` or `class` in
`workspace/main.py`).

---

## Backlog: Audit Miss Rate at CRITICAL Tier — Assertion-Level Comparison Required (Sprint 27)

Sprint 27 pre-flight surfaced 2 CRITICAL-class requirements missed by the Sprint 25 audit (`oop-mini` `@property`, `functions-contracts` `name.strip()`). ~28% miss rate at the CRITICAL tier.

Before applying the audit methodology to `world-sql`, `world-js`, or other worlds, the audit script needs assertion-by-assertion comparison logic against grading tests, not just doc-level concept matching.

---

## Backlog: Seeder Propagation — Manual Re-seed Gap (Sprint 27)

Manual re-seed required after every questpack JSON change. Backlog: backend startup check that warns if questpack file mtime > DB row `updated_at`.
