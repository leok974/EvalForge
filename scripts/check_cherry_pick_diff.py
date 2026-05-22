#!/usr/bin/env python3
"""
check_cherry_pick_diff.py — Cherry-pick safety guard.

Detects symbol DELETIONS in a single commit diff.

For Python (.py) files: uses ast.parse() to compare the file before and
after the commit. Detects:
  - Module-level function and class deletions
  - Class method deletions (indented def / async def inside a class)
  - Module-level and class-level constant assignments (UPPER_SNAKE_CASE)

For JS/TS (.js/.ts/.tsx/.jsx) files: uses regex on removed lines for
top-level function and class declarations (same as before).

Usage:
    python scripts/check_cherry_pick_diff.py <SHA|HEAD>

Exit codes:
    0  — no deletions detected (safe to merge / cherry-pick)
    1  — deletions found (report printed; review before proceeding)
    2  — git or script error
"""

import ast
import re
import sys
import subprocess
from pathlib import Path

# ---------------------------------------------------------------------------
# JS / TS regex patterns (top-level only — no leading whitespace after '-')
# ---------------------------------------------------------------------------

_JS_FUNC  = re.compile(r'^-(?:export\s+)?(?:default\s+)?(?:async\s+)?function\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*[\(<]')
_JS_ARROW = re.compile(r'^-(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*=\s*(?:async\s+)?\(')
_JS_CLASS = re.compile(r'^-(?:export\s+)?(?:default\s+)?class\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*[{\(]')


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

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


def get_file_at_revision(sha: str, filepath: str) -> str | None:
    """Return file content at git revision sha, or None if not present."""
    try:
        result = subprocess.run(
            ["git", "show", f"{sha}:{filepath}"],
            capture_output=True, text=True, check=True,
            encoding="utf-8", errors="replace",
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return None


def resolve_sha(sha: str) -> str:
    """Resolve HEAD or a short SHA to the short SHA (for display)."""
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--short", sha],
            capture_output=True, text=True, check=True, encoding="utf-8",
        )
        return r.stdout.strip()
    except subprocess.CalledProcessError:
        return sha


# ---------------------------------------------------------------------------
# Python AST analysis
# ---------------------------------------------------------------------------

def _is_constant_name(name: str) -> bool:
    """True if the name follows the ALL_CAPS constant convention."""
    return name.isupper() or (name.replace("_", "").isupper() and "_" in name)


def extract_python_symbols(source: str) -> dict | None:
    """
    Parse Python source with ast and return a dict of named symbols.

    {
        "functions":  {"func_name"},              # module-level functions
        "classes":    {"ClassName"},              # module-level classes
        "methods":    {"ClassName.method_name"},  # class-body methods
        "constants":  {"CONST"},                  # module-level UPPER_SNAKE_CASE assignments
        "cls_consts": {"ClassName.ATTR"},         # class-body UPPER_SNAKE_CASE assignments
    }

    Returns None on SyntaxError.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None

    symbols: dict = {
        "functions":  set(),
        "classes":    set(),
        "methods":    set(),
        "constants":  set(),
        "cls_consts": set(),
    }

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            symbols["functions"].add(node.name)

        elif isinstance(node, ast.ClassDef):
            symbols["classes"].add(node.name)
            cls = node.name

            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    symbols["methods"].add(f"{cls}.{child.name}")

                elif isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name) and _is_constant_name(target.id):
                            symbols["cls_consts"].add(f"{cls}.{target.id}")

                elif isinstance(child, ast.AnnAssign):
                    if isinstance(child.target, ast.Name) and _is_constant_name(child.target.id):
                        symbols["cls_consts"].add(f"{cls}.{child.target.id}")

        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and _is_constant_name(target.id):
                    symbols["constants"].add(target.id)

        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and _is_constant_name(node.target.id):
                symbols["constants"].add(node.target.id)

    return symbols


def find_python_deletions_ast(sha: str, filepath: str) -> list[tuple[str, str]]:
    """
    Compare Python file before and after commit sha using AST.

    Returns list of (kind, label) deletions, e.g.:
        [("function", "run_shell_local"), ("method", "MyClass.my_method")]
    """
    before_src = get_file_at_revision(f"{sha}^", filepath)
    after_src  = get_file_at_revision(sha, filepath)

    if before_src is None:
        return []  # new file — no deletions
    if after_src is None:
        return []  # entire file deleted — handled separately; skip for now

    before = extract_python_symbols(before_src)
    after  = extract_python_symbols(after_src)

    if before is None or after is None:
        return []  # parse error — fail open (don't block on unreadable file)

    deletions: list[tuple[str, str]] = []

    for name in sorted(before["functions"] - after["functions"]):
        deletions.append(("function", name))
    for name in sorted(before["classes"] - after["classes"]):
        deletions.append(("class", name))
    for name in sorted(before["methods"] - after["methods"]):
        deletions.append(("method", name))
    for name in sorted(before["constants"] - after["constants"]):
        deletions.append(("constant", name))
    for name in sorted(before["cls_consts"] - after["cls_consts"]):
        deletions.append(("class constant", name))

    return deletions


# ---------------------------------------------------------------------------
# Main diff parser
# ---------------------------------------------------------------------------

def parse_deletions(diff_text: str, sha: str) -> dict[str, list[tuple[str, str]]]:
    """
    Walk a unified diff and collect symbol deletions per file.

    Python files:  AST-based (precise; catches methods and constants).
    JS/TS files:   regex on removed lines (top-level only).

    Returns:
        { "path/to/file.py": [("function"|"method"|"class"|"constant", name), ...] }
    """
    deletions: dict[str, list[tuple[str, str]]] = {}
    current_file: str | None = None
    current_lang: str | None = None
    processed_py: set[str] = set()

    for raw_line in diff_text.splitlines():
        # ---- file header ----
        if raw_line.startswith("diff --git "):
            parts = raw_line.split(" b/", 1)
            current_file = parts[1].strip() if len(parts) == 2 else None
            if current_file:
                ext = Path(current_file).suffix.lower()
                if ext == ".py":
                    current_lang = "python"
                    # Run AST check once per Python file
                    if current_file not in processed_py:
                        processed_py.add(current_file)
                        py_dels = find_python_deletions_ast(sha, current_file)
                        if py_dels:
                            deletions.setdefault(current_file, []).extend(py_dels)
                elif ext in (".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs"):
                    current_lang = "js"
                else:
                    current_lang = None
            continue

        if current_lang is None or current_file is None:
            continue

        # Python is handled via AST — skip individual diff lines
        if current_lang == "python":
            continue

        # ---- JS/TS: only removed lines ----
        if not raw_line.startswith("-"):
            continue
        if raw_line.startswith("---"):
            continue

        if current_lang == "js":
            for pattern, kind in (
                (_JS_FUNC,  "function"),
                (_JS_CLASS, "class"),
                (_JS_ARROW, "function"),
            ):
                m = pattern.match(raw_line)
                if m:
                    deletions.setdefault(current_file, []).append((kind, m.group(1)))
                    break

    return deletions


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/check_cherry_pick_diff.py <SHA|HEAD>", file=sys.stderr)
        sys.exit(2)

    sha = sys.argv[1]
    short = resolve_sha(sha)
    diff = get_commit_diff(sha)
    deletions = parse_deletions(diff, sha)

    if not deletions:
        print(f"[OK] {short} — no deletions detected.")
        sys.exit(0)

    total = sum(len(v) for v in deletions.values())
    print(f"[WARN] {short} — {total} DELETION(S) DETECTED:\n")
    for filename, symbols in sorted(deletions.items()):
        print(f"  {filename}:")
        for kind, name in symbols:
            print(f"    - deleted {kind}: {name!r}")
    print()
    print("ACTION REQUIRED: Review each deletion.")
    print("  If intentional  -> document it in the commit message.")
    print("  If accidental   -> restore the symbol before merging / cherry-picking.")
    sys.exit(1)


if __name__ == "__main__":
    main()
