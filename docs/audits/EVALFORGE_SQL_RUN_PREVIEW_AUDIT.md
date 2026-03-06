# EvalForge SQL Run Preview & Architecture Audit

## 1. Quest Runtime Pipeline Map
EvalForge defines two distinct execution pathways for quests: **Run** (Preview) and **Submit** (Grading).

### Run (Preview) vs Submit (Grading)
*   **Run**: Triggered manually by the user to quickly preview code effects without grading. It drops `--tests` flags and relies directly on the language environment or a preview fallback to generate `artifacts`.
*   **Submit**: Triggers the deterministic grading harness, injecting `test_*.py` files, evaluating objectives, and committing the `QuestAttempt` to the database with a pass/fail status.

### Pipeline Source of Truth
*   **Language Detection**: Key_terms only drive Codex linking; language is persisted from questpack `language` during seeding. The runtime uses the DB `quests.language` as the single source of truth.
*   **Workspace Hydration Precedence**:
    1. If `payload.workspace_files` exists and includes `task.sql`, that wins.
    2. Else fall back to DB/disk workspace `workspace_json`.
    *Note: `Run` must always extract SQL from `task.sql` (or `payload.code`), never from whatever the "active file" happens to be.*
*   **Artifact Propagation**: Artifacts are constructed **in memory** and returned directly in the API response; disk writes are an optional best-effort conditionally written to `/tmp/evalforge_artifacts/<attempt_id>`. File I/O must never gate UI visibility.

---

## 2. SQL-Specific Risks & Hotspots (Resolved & Outstanding)

### Resolved P0 Risks
*   **File Permissions (Write Denied)**: The artifact extraction previously wrote JSON directly to the readonly `td` directory inside Docker, crashing on `Errno 13`.
    *   *Fix Applied*: Mapped a completely safe temporary directory `/tmp/evalforge_artifacts/<attempt_id>` using `EVALFORGE_ARTIFACTS_DIR`.
*   **Regex String Parsing for Result Sets**: The SQL test harness guessed if a statement returned rows using `stmt.lstrip().upper().startswith("SELECT")`. This broke heavily on CTEs (`WITH`) or queries prefixed with `-- comments`.
    *   *Fix Applied*: Tests now natively bind to `sqlite3.Cursor.description` directly, securely confirming true SQL result sets.
*   **Empty Artifact Defaults**: Execution timeouts previously returned `artifacts: null`, crashing the frontend blindly.
    *   *Fix Applied*: The API explicitly injects default empty states for `sql_student_result`, `sql_trace`, and `sql_explain` if they collapse.

### Outstanding Debt Hotspots
*   **`arcade_app/services/run_unittest_json.py`**: Currently acts as a monolithic dump zone for both standard Python testing *and* the SQL fallback runner. SQL logic shouldn't live inside the Python `unittest` module.

---

## 3. Layouts Deprecation Assessment
Currently, EvalForge operates using multiple UI components conditionally rendered via system routes (e.g., `WorkbenchLayout`, `Cyberdeck`, `Orion`).

### Impact
*   Features like `QuestIDE`, `CoachPanel`, and `Intent Oracle` are duplicated or conditionally wired across layout boundaries, causing regression risks when adding new tabs (like `Query Result`).

### Proposed Migration Plan: Single "Workbench"
1.  **Consolidate Tools**: Move all persistent dev tools (Query Trace, Live Previews, Terminal) into the standardized `Terminal Tabs` component.
2.  **Abstract Codex**: Ensure the Codex is always accessible globally via a drawer mechanism instead of consuming grid space in specific layouts.
3.  **Deprecate Right Panels**: Remove the standalone Intent Oracle / right-hand panels, standardizing them as Terminal artifacts.
4.  **Phased Deletion**: Gradually phase out `isCyberdeck` and `isOrion` booleans from root app state mapping, collapsing everything to standard `Bench`.

---

## 4. Proposed "Run Preview" Architecture Refactor
The core architectural debt revolves around **Preview coupling to the Grading Test Harness**. 
Currently, clicking `Run` triggers the *Test Harness* (`run_unittest_json.py`), looks for tests, discovers `0`, and then falls back to a custom branch. 

**Proposal: Independent Preview Runners**
We must conceptually split the registry execution commands for `Run` and `Submit`.
1.  **Creation**: `runners/sql_preview.py`, `runners/web_preview.py`, `runners/python_preview.py`.
2.  **Dispatch**: If `mode == "run"`, `runner_registry.py` explicitly executes the `_preview.py` variant.
3.  **Result**: The Preview Runners solely exist to parse the user's base code, execute any setup fixtures, ignore tests completely, and dump UI-compatible `artifacts.*` JSON to the safe temp directory.

This guarantees tests can evolve independently without breaking browser preview contracts.

---

## 5. Quest Content Consistency: `sql-select`
The SQL Foundations introductory quest (`sql-select`) has been fully promoted to the Golden Exemplar.
- DB `key_terms` explicitly seeded with `["select", "from", "order-by"]`.
- `workspace/task.sql` implements the standard query template skeleton.
- Markdown Docs (`briefing, tutorial, hints, lore`) are fully concrete, avoiding placeholder generic test data.

---

## 6. SQL World "Golden Exemplar" Acceptance Criteria
To prove `sql-select` is truly golden:
1. `GET /api/quests/sql-select` returns `language: "sql"` and `workspace_files` contains `task.sql` and fixtures.
2. Clicking **Run** produces:
   - `artifacts.sql_student_result.columns.length > 0`
   - `artifacts.sql_student_result.rows.length > 0` (given seed data)
   - `artifacts.sql_trace` present (can be empty list but must exist)
3. UI behavior: auto-switch to **Query Result** tab when `sql_student_result` exists.
