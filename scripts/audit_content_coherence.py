#!/usr/bin/env python3
"""
Sprint 24: Content Coherence Audit — world-python
Checks within-quest file contradictions: main.py vs task.py vs example.py vs briefing.md.

Usage:
    python scripts/audit_content_coherence.py
Output:
    docs/audits/CONTENT_COHERENCE_AUDIT.md
"""

from __future__ import annotations
import ast
import json
import re
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent

ACTIVE_PYTHON_PACKS = [
    "data/questpacks/foundry_python.json",
    "data/questpacks/python_systems.json",
    "data/questpacks/_tier2/python_tier2.json",
    "data/questpacks/python_selenium.json",
]

# Selenium quests use main.py as the driver script, not a stub — skip function checks
SELENIUM_TRACK = "python-selenium"

OUTPUT_PATH = ROOT / "docs/audits/CONTENT_COHERENCE_AUDIT.md"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_quests(pack_path: Path) -> list[dict]:
    data = json.loads(pack_path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "quests" in data:
        return data["quests"]
    return []


def resolve_workspace(pack_path: Path, quest: dict) -> Optional[Path]:
    ws = quest.get("workspace", {})
    files_from = ws.get("files_from")
    if not files_from:
        return None
    candidate = (pack_path.parent / files_from).resolve()
    return candidate if candidate.exists() else None


def read_file(path: Path, fname: str) -> Optional[str]:
    f = path / fname
    if not f.exists():
        return None
    try:
        return f.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None


def extract_top_level_functions(code: str) -> list[str]:
    """Return names of top-level def statements (not nested)."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        # Fallback to regex for unparseable stubs (e.g. raise NotImplementedError at top)
        return re.findall(r"^def\s+(\w+)\s*\(", code, re.MULTILINE)
    return [
        node.name
        for node in ast.iter_child_nodes(tree)
        if isinstance(node, ast.FunctionDef)
    ]


def is_stub_body(code: str, fn_name: str) -> bool:
    """True if fn_name's body is a stub (pass, raise NotImplementedError, # TODO)."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return "TODO" in code or "pass" in code
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) and node.name == fn_name:
            body = node.body
            if len(body) == 1:
                stmt = body[0]
                # pass
                if isinstance(stmt, ast.Pass):
                    return True
                # raise NotImplementedError(...)
                if isinstance(stmt, ast.Raise):
                    return True
                # Expr containing a string (docstring only)
                if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
                    return True
            if len(body) == 2:
                # docstring + pass/raise
                if isinstance(body[1], (ast.Pass, ast.Raise)):
                    return True
    return False


def has_main_wrapper_antipattern(code: str) -> bool:
    """True if main.py uses `def main():` containing only pass (empty wrapper)."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            body = node.body
            # Whole body is a single pass or a comment-comment (ellipsis/pass)
            if len(body) == 1 and isinstance(body[0], ast.Pass):
                return True
            # body has comments+pass (comments aren't AST nodes, so just check
            # if there's ONLY pass at the end and no real logic)
            non_trivial = [
                s for s in body
                if not isinstance(s, (ast.Pass, ast.Expr))
                or (isinstance(s, ast.Expr) and not isinstance(s.value, ast.Constant))
            ]
            if not non_trivial:
                return True
    return False


def extract_comma_sep_output_pattern(code: str) -> bool:
    """True if code expects comma-separated output (join(",") or join(","))."""
    return bool(re.search(r'["\'],["\']\s*\.\s*join|\.join\(.*["\'],["\']\)', code))


def extract_per_line_loop_prints(code: str) -> bool:
    """True if code uses a for-loop to print each value separately."""
    return bool(re.search(r"for\s+\w+\s+in\s+\w+[\s\S]{0,50}?print\(", code))


def find_concept_terms(code: str) -> set[str]:
    """Pull identifiers and string literals from code for briefing cross-check."""
    terms: set[str] = set()
    # function names
    terms.update(re.findall(r"def\s+(\w+)\s*\(", code))
    # key identifiers in assignments / calls
    terms.update(re.findall(r"\b([a-z_][a-z0-9_]{3,})\b", code))
    return terms


# ---------------------------------------------------------------------------
# Per-quest checks
# ---------------------------------------------------------------------------

Finding = dict  # {type, severity, detail}


def is_inline_starter_quest(quest: dict) -> bool:
    """True for quests where starter_code lives in the JSON (no main.py in workspace)."""
    # These quests have grading_json.entrypoint = "task.py" and inline starter_code
    grading = quest.get("grading_json", {})
    has_inline_starter = bool(quest.get("starter_code"))
    has_task_entrypoint = grading.get("entrypoint") == "task.py"
    return has_inline_starter or has_task_entrypoint


def check_quest(quest: dict, workspace: Path) -> list[Finding]:
    findings: list[Finding] = []
    slug = quest.get("slug", "?")
    track = quest.get("track_id", "")

    main  = read_file(workspace, "main.py")
    task  = read_file(workspace, "task.py")
    ex    = read_file(workspace, "example.py")
    brief = read_file(workspace, "briefing.md")

    # --- Missing files ---
    # Tier2/ignition quests use inline starter_code in the questpack JSON and
    # have no main.py in the workspace by design. Suppress that case.
    inline_starter = is_inline_starter_quest(quest)
    for fname, content in [("main.py", main), ("example.py", ex)]:
        if content is None:
            if fname == "main.py" and inline_starter:
                continue  # Expected: no main.py for inline-starter quests
            findings.append({"type": "MISSING_FILE", "severity": "warn",
                              "detail": f"{fname} not found in workspace"})

    # Selenium quests: skip function-level structural checks (main.py IS the solution driver)
    if track == SELENIUM_TRACK:
        return findings

    # --- 1. Starter coherence: main.py has wrong function stubs ---
    if task and main:
        task_fns = [f for f in extract_top_level_functions(task)
                    if f not in ("main", "setUp", "tearDown", "setUpClass", "tearDownClass")
                    and not f.startswith("test_")]
        main_fns = extract_top_level_functions(main)
        main_fns_non_main = [f for f in main_fns if f != "main"]

        # Functions required by task.py that are missing from main.py
        missing_stubs = [f for f in task_fns if f not in main_fns]
        if missing_stubs:
            findings.append({
                "type": "MISSING_STUBS",
                "severity": "error",
                "detail": (
                    f"task.py requires {task_fns} but main.py only defines {main_fns}. "
                    f"Missing stubs: {missing_stubs}"
                )
            })

        # Functions in main.py that don't appear in task.py (likely copy-paste from a different quest)
        stray_fns = [f for f in main_fns_non_main if f not in task_fns]
        if stray_fns and task_fns:
            findings.append({
                "type": "STRAY_STUB",
                "severity": "error",
                "detail": (
                    f"main.py defines {stray_fns} which are NOT in task.py. "
                    f"Likely wrong stub copied from another quest."
                )
            })

    # --- 2. Empty wrapper antipattern (def main(): pass) ---
    if main and has_main_wrapper_antipattern(main):
        # Only flag if example.py does NOT use a wrapper
        ex_fns = extract_top_level_functions(ex) if ex else []
        if "main" not in ex_fns:
            findings.append({
                "type": "WRAPPER_ANTIPATTERN",
                "severity": "warn",
                "detail": (
                    "main.py wraps starter code in `def main(): pass` "
                    "but example.py is bare module-level code. "
                    "Learner sees a wrapper that example.py doesn't use."
                )
            })

    # --- 3. Output format mismatch: task expects comma-sep, example prints per-line ---
    if task and ex:
        task_comma = extract_comma_sep_output_pattern(task)
        ex_per_line = extract_per_line_loop_prints(ex)
        if task_comma and ex_per_line:
            findings.append({
                "type": "OUTPUT_FORMAT_MISMATCH",
                "severity": "error",
                "detail": (
                    "task.py expects comma-separated output (join) "
                    "but example.py prints each value on its own line. "
                    "Submitting example.py would fail the objective."
                )
            })

        # Reverse: task expects per-line, example does comma-sep
        task_per_line = extract_per_line_loop_prints(task)
        ex_comma = extract_comma_sep_output_pattern(ex)
        if task_per_line and ex_comma:
            findings.append({
                "type": "OUTPUT_FORMAT_MISMATCH",
                "severity": "warn",
                "detail": (
                    "task.py expects per-line output "
                    "but example.py uses comma-separated join. "
                    "Example would produce wrong output."
                )
            })

    # --- 4. Example would not satisfy task's objective ---
    # NOTE: example.py intentionally shows a RELATED but DIFFERENT pattern.
    # For systems quests, example.py deliberately uses different function names to
    # avoid giving away the solution. This check is INFO-only, not actionable by itself.
    if task and ex and main:
        # Check: does example.py define the same functions as task.py requires?
        task_fns_local = [f for f in extract_top_level_functions(task)
                          if f not in ("main", "setUp", "tearDown")
                          and not f.startswith("test_")]
        ex_fns = extract_top_level_functions(ex)
        ex_missing = [f for f in task_fns_local if f not in ex_fns]
        if ex_missing and task_fns_local:
            findings.append({
                "type": "EXAMPLE_MISSING_FUNCTIONS",
                "severity": "info",  # Not actionable: example shows a related pattern by design
                "detail": (
                    f"example.py doesn't define {ex_missing} which task.py requires. "
                    f"By design: example shows a related pattern, not the exact solution."
                )
            })

    # --- 5. Briefing mentions function names not in task.py ---
    if brief and task:
        task_fns_local = [f for f in extract_top_level_functions(task)
                          if not f.startswith("test_") and f not in ("main", "setUp", "tearDown")]
        # Find function-looking words in briefing that aren't in task.py
        briefing_fn_refs = set(re.findall(r'`(\w+)\(', brief))  # `func(` pattern in markdown
        stray_briefing_fns = briefing_fn_refs - set(task_fns_local) - {"main", "print", "len", "range", "str", "int"}
        task_fns_not_in_brief = [f for f in task_fns_local if f not in brief]
        if stray_briefing_fns:
            findings.append({
                "type": "BRIEFING_STRAY_FUNCTION",
                "severity": "info",
                "detail": (
                    f"briefing.md references functions {sorted(stray_briefing_fns)} "
                    f"not required by task.py. May confuse learners."
                )
            })
        if task_fns_not_in_brief and task_fns_local:
            findings.append({
                "type": "BRIEFING_MISSING_FUNCTION",
                "severity": "info",
                "detail": (
                    f"task.py requires {task_fns_local} "
                    f"but briefing.md doesn't mention them. "
                    f"Missing from briefing: {task_fns_not_in_brief}"
                )
            })

    return findings


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    all_results: list[dict] = []
    total_quests = 0
    flagged_quests = 0

    for pack_rel in ACTIVE_PYTHON_PACKS:
        pack_path = ROOT / pack_rel
        if not pack_path.exists():
            print(f"WARN: {pack_rel} not found, skipping", file=sys.stderr)
            continue

        quests = load_quests(pack_path)
        for quest in quests:
            slug = quest.get("slug", "?")
            workspace = resolve_workspace(pack_path, quest)
            if workspace is None:
                all_results.append({
                    "slug": slug,
                    "pack": pack_rel,
                    "track": quest.get("track_id", ""),
                    "title": quest.get("title", slug),
                    "workspace": None,
                    "findings": [{"type": "NO_WORKSPACE", "severity": "warn",
                                  "detail": "workspace directory not found on disk"}]
                })
                flagged_quests += 1
                total_quests += 1
                continue

            total_quests += 1
            findings = check_quest(quest, workspace)
            result = {
                "slug": slug,
                "pack": pack_rel,
                "track": quest.get("track_id", ""),
                "title": quest.get("title", slug),
                "workspace": str(workspace.relative_to(ROOT)),
                "findings": findings,
            }
            all_results.append(result)
            if findings:
                flagged_quests += 1

    # --- Write report ---
    lines: list[str] = []
    lines.append("# Content Coherence Audit — world-python")
    lines.append("")
    lines.append(f"**Generated:** Sprint 24  ")
    lines.append(f"**Scope:** Active Python questpacks  ")
    lines.append(f"**Quests audited:** {total_quests}  ")
    lines.append(f"**Quests flagged:** {flagged_quests}  ")
    lines.append(f"**Quests clean:** {total_quests - flagged_quests}  ")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Group: errors first, then warns, then info
    severity_order = {"error": 0, "warn": 1, "info": 2}
    flagged = [r for r in all_results if r["findings"]]
    clean   = [r for r in all_results if not r["findings"]]

    if flagged:
        lines.append(f"## Flagged Quests ({len(flagged)})")
        lines.append("")

        # Sort by worst severity
        def worst_severity(r: dict) -> int:
            sevs = [severity_order.get(f["severity"], 3) for f in r["findings"]]
            return min(sevs) if sevs else 3

        flagged.sort(key=worst_severity)

        for r in flagged:
            title = r["title"]
            slug = r["slug"]
            track = r["track"]
            ws = r["workspace"] or "N/A"
            lines.append(f"### `{slug}` — {title}")
            lines.append(f"**Track:** `{track}` | **Workspace:** `{ws}`")
            lines.append("")
            for f in r["findings"]:
                sev = f["severity"].upper()
                icon = {"ERROR": "🔴", "WARN": "🟡", "INFO": "🔵"}.get(sev, "⚪")
                lines.append(f"- {icon} **{f['type']}**: {f['detail']}")
            lines.append("")

    lines.append("---")
    lines.append("")
    if clean:
        lines.append(f"## Clean Quests ({len(clean)})")
        lines.append("")
        for r in clean:
            lines.append(f"- ✅ `{r['slug']}` ({r['track']})")
        lines.append("")

    report = "\n".join(lines)
    OUTPUT_PATH.write_text(report, encoding="utf-8")
    print(f"Report written to {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Audited {total_quests} quests — {flagged_quests} flagged, {total_quests - flagged_quests} clean")

    # Stop condition: > 30 need fixes
    error_count = sum(
        1 for r in flagged
        if any(f["severity"] == "error" for f in r["findings"])
    )
    if error_count > 30:
        print(f"\n⚠️  STOP CONDITION: {error_count} quests have ERROR-level findings.")
        print("Scope may need to expand to a multi-sprint effort. Review before fixing.")
        sys.exit(2)


if __name__ == "__main__":
    main()
