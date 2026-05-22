#!/usr/bin/env python3
"""
check_cherry_pick_diff.py — Cherry-pick safety guard.

Detects top-level function/class DELETIONS in a single commit diff.
Use before or after cherry-picking to catch silent symbol removal.

Usage:
    python scripts/check_cherry_pick_diff.py <SHA|HEAD>

Exit codes:
    0  — no top-level deletions detected (safe to merge / cherry-pick)
    1  — deletions found (report printed; review before proceeding)
    2  — git or script error
"""

import re
import sys
import subprocess
from pathlib import Path

# ---------------------------------------------------------------------------
# Patterns: line must start with '-' (deleted), not '-   ' (indented body),
# so we anchor to the removal marker followed immediately by the keyword.
# ---------------------------------------------------------------------------

# Python: top-level only — no leading whitespace after '-'
_PY_DEF   = re.compile(r'^-(?:async )?def ([A-Za-z_][A-Za-z0-9_]*)\s*[\(:]')
_PY_CLASS = re.compile(r'^-class ([A-Za-z_][A-Za-z0-9_]*)\s*[:\(]')

# JS / TS: top-level function declarations and class declarations
_JS_FUNC  = re.compile(r'^-(?:export\s+)?(?:default\s+)?(?:async\s+)?function\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*[\(<]')
_JS_ARROW = re.compile(r'^-(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*=\s*(?:async\s+)?\(')
_JS_CLASS = re.compile(r'^-(?:export\s+)?(?:default\s+)?class\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*[{\(]')


def get_commit_diff(sha: str) -> str:
    """Return the unified diff of a single commit (parent..sha)."""
    try:
        result = subprocess.run(
            ["git", "show", sha, "--unified=0", "--diff-filter=DM", "--no-color"],
            capture_output=True, text=True, check=True,
            encoding="utf-8", errors="replace",
        )
        return result.stdout
    except subprocess.CalledProcessError as exc:
        print(f"[ERROR] git show {sha!r} failed:\n{exc.stderr.strip()}", file=sys.stderr)
        sys.exit(2)


def parse_deletions(diff_text: str) -> dict[str, list[tuple[str, str]]]:
    """
    Walk a unified diff and collect top-level symbol deletions.

    Returns:
        { "path/to/file.py": [("function"|"class", "symbol_name"), ...] }
    """
    deletions: dict[str, list[tuple[str, str]]] = {}
    current_file: str | None = None
    current_lang: str | None = None  # "python" | "js" | None

    for raw_line in diff_text.splitlines():
        # ---- detect file header ----
        if raw_line.startswith("diff --git "):
            # e.g. "diff --git a/arcade_app/foo.py b/arcade_app/foo.py"
            parts = raw_line.split(" b/", 1)
            current_file = parts[1].strip() if len(parts) == 2 else None
            if current_file:
                ext = Path(current_file).suffix.lower()
                if ext == ".py":
                    current_lang = "python"
                elif ext in (".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs"):
                    current_lang = "js"
                else:
                    current_lang = None
            continue

        if current_lang is None or current_file is None:
            continue

        # ---- only care about removed lines ----
        if not raw_line.startswith("-"):
            continue
        # skip the "--- a/file" diff header line
        if raw_line.startswith("---"):
            continue

        line = raw_line  # keep the leading '-' for regex anchoring

        if current_lang == "python":
            m = _PY_DEF.match(line)
            if m:
                deletions.setdefault(current_file, []).append(("function", m.group(1)))
                continue
            m = _PY_CLASS.match(line)
            if m:
                deletions.setdefault(current_file, []).append(("class", m.group(1)))
                continue

        elif current_lang == "js":
            for pattern, kind in ((_JS_FUNC, "function"), (_JS_CLASS, "class"), (_JS_ARROW, "function")):
                m = pattern.match(line)
                if m:
                    deletions.setdefault(current_file, []).append((kind, m.group(1)))
                    break

    return deletions


def resolve_sha(sha: str) -> str:
    """Resolve HEAD or a short SHA to the full SHA (for display)."""
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--short", sha],
            capture_output=True, text=True, check=True, encoding="utf-8",
        )
        return r.stdout.strip()
    except subprocess.CalledProcessError:
        return sha


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/check_cherry_pick_diff.py <SHA|HEAD>", file=sys.stderr)
        sys.exit(2)

    sha = sys.argv[1]
    short = resolve_sha(sha)
    diff = get_commit_diff(sha)
    deletions = parse_deletions(diff)

    if not deletions:
        print(f"[OK] {short} — no top-level function/class deletions detected.")
        sys.exit(0)

    # Deletions found — print a structured report
    total = sum(len(v) for v in deletions.values())
    print(f"[WARN] {short} — {total} TOP-LEVEL DELETION(S) DETECTED:\n")
    for filename, symbols in sorted(deletions.items()):
        print(f"  {filename}:")
        for kind, name in symbols:
            print(f"    - deleted {kind}: {name!r}")
    print()
    print("ACTION REQUIRED: Review each deletion.")
    print("  If intentional  -> add a comment in the commit message documenting why.")
    print("  If accidental   -> restore the symbol before merging / cherry-picking.")
    sys.exit(1)


if __name__ == "__main__":
    main()
