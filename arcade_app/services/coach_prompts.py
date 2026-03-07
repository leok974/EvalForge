
EXPLAIN_SYSTEM_PROMPT = """
You are the EvalForge Coach, an AI coding tutor.
Your goal is to EXPLAIN the concepts and implementation details to the student.

MODE: EXPLAIN

GUIDELINES:
1. Read the [ENTRYPOINT] file first — that is the student's primary work file.
2. Explain the CORE CONCEPTS relevant to the code.
3. If run_passed=true: celebrate success briefly, then explain WHY the code works. Do NOT propose edits, patches, or diffs.
4. If the code is incomplete (TODOs), explain what needs to be done conceptually.
5. If there are errors, explain WHY they might be happening conceptually.
6. Do NOT provide a direct code patch or solution diff. Focus on teaching.
7. 'next_steps' should be a checklist of high-level, conceptual actions only.
8. 'hypotheses' should be educational observations about the current state.
9. NEVER reference a file other than the entrypoint as the primary subject.

OUTPUT FORMAT:
Return a JSON object matching the `CoachResponse` schema.
"""

DEBUG_SYSTEM_PROMPT = """
You are the EvalForge Coach, an AI coding tutor.
Your goal is to DEBUG the student's current failure.

MODE: DEBUG

GUIDELINES:
1. Read the [ENTRYPOINT] file first — that is the ONLY file the student edits.
2. Analyze 'terminal_output_text', 'failing_tests_text', 'runner_result', and the [ENTRYPOINT] file.
3. Identify the ROOT CAUSE of the failure using ONLY evidence from the logs.
4. Any edit suggestion MUST target the ENTRYPOINT file — never any other file.
5. If 'student_mode' is TRUE, do NOT provide a 'patch'. Guide via 'next_steps' only.
6. Do NOT use diff markers (+++/---) in summary_md.
7. If run_passed=true: do NOT suggest edits. Return an empty next_steps list.

EVIDENCE ENFORCEMENT:
- Populate 'evidence' with exact lines from terminal_output_text or failing_tests_text.
- Only state a root cause if you can quote the exact log line(s) that prove it.

TARGET ENFORCEMENT:
- Every next_step with action='edit' MUST have target equal to the ALLOWED_EDIT_TARGETS value.
- If you are unsure which file to edit, always default to the ENTRYPOINT file.

OUTPUT FORMAT:
Return a JSON object matching the `CoachResponse` schema.
Ensure 'primary_error', 'evidence', and 'failure_class' are populated if applicable.
"""

# Default entrypoints per language (fallback when entrypoint_path not sent)
_ENTRYPOINT_DEFAULTS = {
    "sql": "task.sql",
    "python": "task.py",
    "javascript": "task.js",
    "typescript": "task.ts",
    "bash": "task.sh",
    "go": "task.go",
}


def build_user_prompt(data: dict) -> str:
    """Constructs the user message from the request data."""

    quest = data.get("quest_slug", "Unknown Quest")
    language = data.get("language", "")
    all_files = data.get("workspace_files", [])
    tests = data.get("failing_tests_text", "No test output provided.")
    terminal = data.get("terminal_output_text", "")
    runner = data.get("runner_result", {})
    run_passed = data.get("run_passed", None)

    # Resolve entrypoint — explicit > language default > "task.sql"
    entrypoint = (
        data.get("entrypoint_path")
        or _ENTRYPOINT_DEFAULTS.get(language, "task.sql")
    )

    # Split files: entrypoint first, rest as reference
    entrypoint_files = [f for f in all_files if f.get("path", "").endswith(entrypoint)]
    reference_files = [f for f in all_files if not f.get("path", "").endswith(entrypoint)
                       and not _is_fixture(f.get("path", ""))]

    prompt = f"Quest: {quest}\n"
    prompt += f"Language: {language or 'unknown'}\n"
    prompt += f"Run Passed: {run_passed}\n"
    prompt += f"ENTRYPOINT_PATH: {entrypoint}\n"
    prompt += f"ALLOWED_EDIT_TARGETS: [{entrypoint}]\n\n"

    # Entrypoint file (highest priority — model must read this first)
    if entrypoint_files:
        prompt += "## [ENTRYPOINT] Primary Student File\n"
        for f in entrypoint_files:
            prompt += f"--- {f.get('path')} ---\n{f.get('content', '')}\n\n"
    else:
        prompt += f"## [ENTRYPOINT] Note: Entrypoint file '{entrypoint}' not found in workspace.\n\n"

    # Reference files (secondary context only)
    if reference_files:
        prompt += "## [REFERENCE ONLY — do not edit these]\n"
        for f in reference_files:
            prompt += f"--- {f.get('path')} ---\n{f.get('content', '')}\n\n"

    # SQL-specific: include artifacts if available
    if language == "sql" and isinstance(runner, dict):
        artifacts = runner.get("artifacts", {}) or {}
        sr = artifacts.get("sql_student_result", {}) or {}
        if sr.get("columns"):
            prompt += "## SQL Query Result (student's last output)\n"
            prompt += f"Columns: {sr.get('columns')}\n"
            rows = sr.get("rows", [])[:5]
            prompt += f"First {len(rows)} rows: {rows}\n"
            prompt += f"Total rows: {sr.get('row_count', 'unknown')}\n\n"

        trace = artifacts.get("sql_trace", [])
        student_stmts = [e for e in trace if isinstance(e, dict) and e.get("phase") == "student"]
        if student_stmts:
            last = student_stmts[-1]
            prompt += "## SQL Statement Executed\n"
            prompt += f"{last.get('sql', '')}\n"
            if last.get("error"):
                prompt += f"Error: {last.get('error')}\n"
            prompt += "\n"

    # Constraints reminder
    prompt += f"## [CONSTRAINTS]\n"
    prompt += f"- Only propose edits to: {entrypoint}\n"
    if run_passed:
        prompt += "- run_passed=true: do NOT propose edits, patches, or diff markers. Explain success only.\n"
    prompt += "\n"

    if terminal:
        prompt += f"## Terminal Output (Primary Source of Truth):\n{terminal}\n\n"

    if tests and tests != "No test output provided.":
        prompt += f"## Failing Tests / Output:\n{tests}\n\n"

    if runner:
        # Trim to short summary (avoid flooding prompt with full runner blob)
        r_summary = {
            "passed": runner.get("passed"),
            "exit_code": runner.get("exit_code"),
            "timed_out": runner.get("timed_out"),
            "objective_results": runner.get("objective_results", [])[:5],
        }
        prompt += f"## Runner Result Summary:\n{r_summary}\n"

    return prompt


def _is_fixture(path: str) -> bool:
    """Mark fixture/schema/seed files as not-for-reference in prompt."""
    keywords = ["fixtures/", "schema.sql", "seed.sql", "grading/", ".pytest_cache"]
    return any(k in path for k in keywords)
