# World-Testing Feasibility Report
## Date: 2026-05-23
## Sprint: Phase 0 — Infrastructure Assessment

This report covers all five investigation tasks from the Phase 0 brief. No quest content was authored.
Small targeted code reads were done; no changes were made. The "Recommended next sprint" section
at the bottom is the actionable output.

---

## 1. `tests_pass` Grader

### Implementation files

| File | Role |
|------|------|
| `arcade_app/services/run_unittest_json.py` | The actual test runner — runs pytest, emits JSON |
| `arcade_app/services/quest_validate.py` (lines 786–852) | Parses the JSON, extracts failure names, populates objective result |
| `arcade_app/quest_helper.py` (lines 292–293) | Normalises `tests_pass` kind during objective loading |

### Test file location

**Hardcoded to `/workspace` (the Docker container path).** pytest is invoked with `/workspace` as
both the test-discovery root and the working directory:

```python
# run_unittest_json.py lines 30-43
proc = subprocess.run(
    [sys.executable, "-m", "pytest",
     WORKSPACE,          # "/workspace" — hardcoded constant (line 17)
     "--tb=short", "-q", "--no-header", "--color=no"],
    cwd=WORKSPACE,
    env={"PYTHONPATH": "/workspace" + os.pathsep + existing_pythonpath},
)
```

pytest's default discovery rules (`test_*.py` / `*_test.py`) apply across the entire workspace
tree. There is **no per-quest configuration** of which test files to target.

### How results are reported

The runner script:
1. Captures all pytest stdout + stderr internally.
2. Parses the summary line with regex to extract `passed` / `failed` counts.
3. Parses `FAILED test_x.py::test_name - <message>` lines to get individual failure names
   and their one-line message.
4. Emits **only the JSON blob** to the runner script's own stdout (last line):
   `{"passed": N, "failed": N, "total": N, "failures": [{"name": "...", "message": "..."}]}`
5. Prints raw pytest output (truncated to 1000 chars) to the runner's **stderr** only.

The `tests_pass` validator in `quest_validate.py` parses the JSON from stdout and sets
`obj.detail` to either `"All N tests passed"` or `"Tests failed: test_a, test_b"` (up to 3
names, then `"and N more"`).

### Failure output to the learner

- **Test names of failures:** VISIBLE — extracted from `FAILED` lines and embedded in
  the objective result detail string.
- **One-line failure message from pytest `FAILED x - msg` line:** PARTIAL — captured in the JSON
  `message` field but **not currently rendered separately** to the learner; only the test name
  appears in the UI detail string (lines 839–850 of `quest_validate.py`).
- **Full `--tb=short` traceback** (assertion details, line numbers, expected vs actual):
  NOT SHOWN — captured to pytest's stdout inside the runner, printed to runner's **stderr**,
  and not surfaced to the frontend. `result.stdout` (line 730 of `QuestIDE.tsx`) only logs
  the JSON blob from the runner's stdout, not the traceback text.

**Example of what a learner sees when a test fails:**

```
Objective: "Unit tests pass"  [FAIL]
Detail: Tests failed: tests/test_math.py::test_addition
```

They do NOT see:
```
FAILED tests/test_math.py::test_addition - assert add(1, 1) == 3
  assert 2 == 3
```

### Verdict: USABLE\_AS\_IS for basic pass/fail gating

The grader works correctly as a gate: all tests pass → quest unlocks; any test fails → quest blocked.
**However, the failure output is pedagogically thin for a testing world.** A learner who writes
a test that fails due to an import error, a wrong assertion, or an exception sees only the test name,
not the reason. For a world where understanding test failure output *is* the learning objective,
this is a meaningful problem.

---

## 2. Nested Workspace Structure

### Findings

**A1 — Seeder (`scripts/questpack_seed.py` lines 131–141):**
Uses `os.walk()` to traverse the workspace directory recursively. Relative paths with forward
slashes are preserved exactly (`inner_path.replace("\\", "/")`). Each file object stored:
```json
{"path": "tests/test_x.py", "content": "...", "editable": true}
```
Nested directories work without any change.

**A2 — Backend storage (`arcade_app/models.py`):**
`workspace_json` is a plain `JSONB` column with no schema constraints. Any nested structure
is accepted. No migration required.

**A3 — Frontend file display (`apps/web/src/components/quests/QuestIDE.tsx` lines 253–259):**
Files are indexed by full path string. Tabs display the full path (e.g.,
`tests/test_ticket_service.py`) as the tab label. There is **no tree UI** — all files appear
as a flat list of tabs, with the `/` visible in the label. For 2–4 files this is readable.
For 8+ files it becomes unwieldy, but world-testing quests are unlikely to exceed 4 files.

**A4 — Runner (`arcade_app/services/code_runner_docker.py`):**
Each file is written to a temp directory with `os.makedirs(dirname, exist_ok=True)`, so
`tests/test_x.py` correctly lands at `<tmpdir>/tests/test_x.py`. pytest is invoked at
`cwd=/workspace` with `PYTHONPATH=/workspace`, so:
- `tests/test_x.py` is discovered by pytest (subdirectory of `/workspace`)
- `from code.ticket_service import ...` works (imports via PYTHONPATH root)

### Verdict table

| Aspect | Status | Evidence |
|--------|--------|----------|
| Seeder handles nested dirs | WORKS | `os.walk()` in `questpack_seed.py:131` |
| Backend accepts nested paths | WORKS | JSONB column, no constraints |
| Frontend renders nested paths | WORKS (with flat tabs) | `QuestIDE.tsx:256` — full path as key |
| pytest discovers `tests/*.py` | WORKS | `cwd=/workspace`, default discovery |
| `from code.x import` works | WORKS | `PYTHONPATH=/workspace` |
| DB migration required | NO | JSONB column already flexible |

### Overall verdict: BUILDABLE\_AS\_DESIGNED

No code changes required to support a `code/ + tests/` workspace layout.

**One UX note:** The file tabs show full paths as flat labels. "tests/test_ticket_service.py"
as a tab label is readable. If the learner's file is not named with the `tests/` prefix,
there is no visual grouping. A future sprint could add a lightweight file tree component,
but it is not required for the first build.

---

## 3. Read-Only File Support

### Evidence found

| File | Line(s) | Finding |
|------|---------|---------|
| `scripts/questpack_seed.py` | 140 | `"editable": True` set on every workspace file object |
| `arcade_app/services/utils.py` | 26–50 | `build_effective_workspace()` passes `editable` flag through |
| `arcade_app/routers/routes_quests_runtime.py` | 273 | Sets `"editable": False` for non-test files in test mode |
| `apps/web/src/components/quests/QuestIDE.tsx` | 241–247 | `isReadOnlyPath()` hardcodes `fixtures/`, `example.sql`, `readme.md` as read-only |
| `apps/web/src/components/quests/QuestIDE.tsx` | 256 | `editable: f.editable ?? true` propagated to frontend state |
| `apps/web/src/components/quests/QuestIDE.tsx` | 1433 | `onChange` guard: `if (!files[activePath]?.editable) return;` |
| `apps/web/src/components/quests/QuestEditor.tsx` | 197–199 | Monaco `readOnly: readOnly` and `domReadOnly: readOnly` wired |

### Classification: Scenario A — Infrastructure Already Wired

The `editable` field exists in the workspace JSON schema, is propagated to the frontend, and
Monaco is configured to respect it. The editor's `onChange` guard prevents silent edits to
read-only files. The mechanism is end-to-end.

**The one gap:** The seeder (`questpack_seed.py:140`) sets `"editable": True` for every file
unconditionally. There is currently no field in the questpack JSON `workspace` block to mark
specific files as non-editable. To make `code/ticket_service.py` read-only, you would need to:

1. Add a `"readonly_files"` list to the questpack `workspace` block:
   ```json
   "workspace": {
     "entrypoint": "tests/test_ticket_service.py",
     "readonly_files": ["code/ticket_service.py", "code/database.py"],
     "files_from": "../../quests/testing-write-your-first-test/workspace"
   }
   ```
2. Update `hydrate_workspace()` in `questpack_seed.py` (≈5 lines) to set
   `"editable": False` for files matching the `readonly_files` list.

**Effort: 1–2 hours.** No DB migration. No frontend change. No Monaco configuration change.
Pure seeder + questpack format extension.

### Recommended approach

Use the `readonly_files` questpack extension described above. It is the cleanest path:
questpack JSON is the source of truth for which files the learner edits; the seeder propagates
the flag to the DB; the frontend and Monaco already handle it correctly.

---

## 4. Boss Grading Mechanics

### How the docker boss combines objectives and rubric

Investigating `data/questpacks/docker_systems.json`, `rubrics/boss-docker-microservice-stack.json`,
`arcade_app/routers/routes_boss.py`, and `arcade_app/grading_helper.py` reveals a
**critical gap** between the questpack format and the actual grading flow:

**What the questpack defines:**
The docker boss quest (`dk-boss-microservice-stack`) in `docker_systems.json` defines
7 deterministic objectives (`yaml_structure` kind) for structural checks on the
submitted Compose file.

**What actually happens at submission:**
1. `POST /api/boss/submit` calls `judge_boss_submission()` in `grading_helper.py`.
2. `judge_boss_with_rubric()` loads the rubric JSON, calls the LLM (Vertex AI / Gemini),
   and returns a `BossEvalResult`.
3. The 7 questpack objectives are **never evaluated**. The `BossDefinition` model has no
   `objectives_json` column. `seed_bosses.py` does not read objectives from the questpack.
4. Win/loss is determined solely by LLM rubric score ≥ 70 (hardcoded in `boss_helper.py:62`).

**The questpack objectives are orphaned.** They are defined in the JSON but have no effect
on the boss fight outcome. The docker boss is currently **rubric-only**.

The rubric itself (4 dimensions × 2 points = 8 max) instructs the LLM to evaluate:
architecture, networking, resilience, and storage — covering the same ground as the deterministic
objectives, but via LLM judgement rather than assertion checks.

### Recommended pattern for a world-testing boss

**Option A (recommended): Pure rubric, no deterministic objectives.**
Keep the boss as rubric-only (consistent with how all current bosses actually work). Design
the rubric dimensions around testing craft: test coverage, assertion quality, edge-case handling,
test independence. This requires zero schema changes.

**Option B: Deterministic objectives as pre-flight gates.**
Add `objectives_json` to `BossDefinition` (DB migration), update `seed_bosses.py` to load
them, and modify `judge_boss_with_rubric()` to run `validate_quest_attempt()` before the LLM
call. If any objective fails, return `score=0` without calling the LLM. Effort: 6–8 hours
including migration.

**For the first world-testing build, use Option A.** The rubric is expressive enough to
evaluate whether the learner's tests are well-designed. Option B is a future infrastructure
improvement that benefits all boss fights, not just world-testing.

### Gotchas for the world-testing boss designer

- **Autofail zeroes the score hard.** Any autofail condition in the rubric triggers
  `total_score = 0` regardless of dimension scores. Use autofails sparingly (e.g.,
  "submitted no test file at all").
- **Win threshold is hardcoded at 70.** This is not configurable per boss.
- **Mock grading** (`EVALFORGE_MOCK_GRADING=1`): any code → score 45 (loss);
  code containing `MAGIC_BOSS_PASS` → score 100 (win). Dev testing of the boss fight
  UI works without real LLM.
- **No `objective_results` on BossRun.** Unlike quest submissions, boss submissions do not
  record per-objective results. If you add deterministic objectives later, you'll need a
  BossRun schema extension too.

---

## 5. Test Output Learner Experience

### Data flow from pytest to the learner

```
pytest (in /workspace, capture_output=True)
  └─ proc.stdout + proc.stderr → parsed for counts + failure names
  └─ JSON summary → printed to runner script stdout (line 104 of run_unittest_json.py)
  └─ Raw pytest output → runner script stderr (first 1000 chars, debug only)

Backend (routes_quests_runtime.py)
  └─ result.stdout = runner script stdout = JSON blob only
  └─ sanitize_logs() applied

Frontend (QuestIDE.tsx line 730)
  └─ addLog(result.stdout, 'output') → terminal tab shows the raw JSON blob
  └─ Objective result detail: "Tests failed: test_name1, test_name2"
```

### What the learner actually sees

| Content | Visible? | Where |
|---------|----------|-------|
| Which tests failed | YES | Objective result detail string |
| Number of passed/failed | YES (in raw JSON in terminal) | Terminal tab (unformatted) |
| One-line message from `FAILED x - msg` | NO (in JSON `message` field, not rendered) | Not surfaced |
| `--tb=short` assertion details | NO | Only in runner stderr, discarded |
| Full pytest stdout | NO | Runner captures it internally |
| Import errors / collection errors | PARTIAL | Shows as "Test error: collecting …" in failure name |

### Why this matters for world-testing pedagogy

A world-testing learner writes `assert add(1, 2) == 4`. The test fails because `add(1,2)` returns
`3`, not `4`. What they currently see:

```
Tests failed: tests/test_math.py::test_add_basic
```

What they need to see to learn:

```
FAILED tests/test_math.py::test_add_basic
  assert result == 4
    where result = add(1, 2) = 3
```

Without the traceback, they must guess why the test failed. For a world whose core learning loop
is "write a test → see it fail → understand the failure → fix it", this is a blocker for
pedagogical effectiveness (though not a technical blocker for building the world).

### The fix

Change `run_unittest_json.py` to include formatted pytest output **in the runner's stdout**
alongside the JSON. The simplest approach: use pytest's `-v` flag and add the raw output to
the JSON payload as a `"raw_output"` field. The validator already passes `stdout` through;
the frontend terminal already renders it.

Alternatively: pipe the `--tb=short` content into the JSON `failures[].message` field instead
of just the one-line `FAILED x - reason` extract.

**Effort: 2–4 hours.** Touches only `run_unittest_json.py` (runner) and optionally
`quest_validate.py` (to surface `message` in the detail string).

### Verdict: NEEDS\_WORK\_FIRST

Not a technical blocker for building world-testing infrastructure. A blocking issue for
**pedagogical effectiveness**: a learner who can't see assertion failures cannot learn
from the testing feedback loop that makes the world meaningful.

---

## Revised Build Estimate

| Scenario | Condition | Estimate |
|----------|-----------|----------|
| Optimistic | All infrastructure as-is; skip traceback fix for v1 | 3 days |
| Realistic | Fix traceback surfacing first; then build world | 4–5 days |
| Pessimistic | Boss deterministic objectives needed; full schema migration | 7–8 days |

**Infrastructure work before content authoring begins:**

| Task | File(s) | Effort | Priority |
|------|---------|--------|----------|
| Surface pytest tracebacks to learner | `run_unittest_json.py` | 2–4 h | HIGH — blocks pedagogy |
| Add `readonly_files` to questpack format + seeder | `questpack_seed.py` | 1–2 h | HIGH — needed for code/ files |
| (Optional) Boss deterministic objectives | `models.py`, `grading_helper.py`, `seed_bosses.py` | 6–8 h | LOW — rubric-only boss works |
| (Optional) File tree UI for nested workspace | `QuestIDE.tsx` | 4–8 h | LOW — flat tabs work for ≤4 files |

---

## Recommended Next Sprint

**Recommendation: FIX\_FIRST, then BUILD.**

Two small infrastructure fixes are needed before content authoring begins:

### Fix 1 — Traceback surfacing (2–4 hours)

File: `arcade_app/services/run_unittest_json.py`

The runner currently captures all pytest output internally and only emits a thin JSON summary.
Include `--tb=short` formatted failure output in the JSON payload so the frontend terminal
can display it. This is the difference between a learner who can learn from test failures
and one who cannot.

```python
# Proposed: add "output" field to summary
summary = {
    "passed": passed,
    "failed": failed,
    "total": passed + failed,
    "failures": errors_list,
    "output": output[:3000],   # raw pytest text, truncated
}
```

Frontend: `QuestIDE.tsx` already renders `result.stdout` in the terminal tab. No frontend
change needed if the raw output is included in the JSON blob (it will appear in the terminal
as part of the JSON string). A cleaner approach would add a dedicated `"test_output"` field
and render it separately, but that requires a small frontend card component.

### Fix 2 — Read-only file support in questpack format (1–2 hours)

File: `scripts/questpack_seed.py`

Extend the `workspace` block in questpack JSON to accept `readonly_files` (a list of paths).
Update `hydrate_workspace()` to set `"editable": False` for matching files. No DB migration,
no frontend change — the full pipeline from seeder → DB → API → frontend → Monaco is
already wired for the `editable` flag.

### After both fixes: BUILD

With these two fixes in place, world-testing is buildable as designed:
- `tests_pass` grader is functional and surfaces pedagogically useful failure output
- Nested `code/ + tests/` workspace layout works end-to-end
- `code/` files can be marked read-only via questpack JSON
- Boss fight uses a rubric (no schema changes needed for v1)
- Learner sees test names + assertion details on failure

Total infrastructure time: **3–6 hours** before content authoring begins.
