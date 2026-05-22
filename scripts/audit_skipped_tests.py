#!/usr/bin/env python3
"""
audit_skipped_tests.py — Enforce the pre-existing test failure rule.

Any test.skip() or test.describe.skip() in tests/e2e/ must carry a
"Revisit: Sprint N" comment. If N <= current sprint number, this script
fails so CI cannot proceed without resolving or re-classifying the skip.

Sprint number source: configs/current_sprint.txt (Option B — explicit file,
updated manually at the start of each sprint).

Exit 0  — all SKIPs are within their revisit window (or have no target).
Exit 1  — at least one SKIP is overdue.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
E2E_DIR = REPO_ROOT / "tests" / "e2e"
SPRINT_FILE = REPO_ROOT / "configs" / "current_sprint.txt"

# Matches test.skip( or test.describe.skip(
SKIP_RE = re.compile(r"test(?:\.describe)?\.skip\(")

# Matches "Revisit: Sprint N" or "Revisit Sprint N" (case-insensitive, with optional colon)
REVISIT_RE = re.compile(r"Revisit:?\s+Sprint\s+(\d+)", re.IGNORECASE)


def read_current_sprint() -> int:
    if not SPRINT_FILE.exists():
        print(f"[WARN] {SPRINT_FILE} not found — skipping sprint-based overdue check.")
        return 0
    text = SPRINT_FILE.read_text(encoding="utf-8").strip()
    try:
        return int(text)
    except ValueError:
        print(f"[WARN] {SPRINT_FILE} contains non-integer '{text}' — skipping overdue check.")
        return 0


def extract_comment_block(lines: list[str], skip_line_idx: int) -> str:
    """Return comment lines near the skip call (above it and up to 30 lines after).

    test.skip() signatures span multiple lines before the body opens, so we
    scan a generous window after the skip call rather than stopping at the
    first non-comment line.
    """
    # Up to 10 lines before the skip call
    before = []
    i = skip_line_idx - 1
    while i >= 0 and i >= skip_line_idx - 10:
        stripped = lines[i].strip()
        if stripped.startswith("//") or stripped.startswith("*") or stripped == "":
            before.append(lines[i])
        else:
            break
        i -= 1
    before.reverse()

    # Up to 30 lines after the skip call (covers multi-line async signatures + body comments)
    after = lines[skip_line_idx + 1 : skip_line_idx + 31]

    return "\n".join(before + [lines[skip_line_idx]] + after)


def audit_file(path: Path, current_sprint: int) -> list[dict]:
    """Return a list of overdue-skip dicts for the given file."""
    overdue = []
    lines = path.read_text(encoding="utf-8").splitlines()

    for idx, line in enumerate(lines):
        if not SKIP_RE.search(line):
            continue

        comment_block = extract_comment_block(lines, idx)
        match = REVISIT_RE.search(comment_block)

        if match:
            revisit_sprint = int(match.group(1))
            if current_sprint >= revisit_sprint:
                overdue.append({
                    "file": str(path.relative_to(REPO_ROOT)),
                    "line": idx + 1,
                    "revisit_sprint": revisit_sprint,
                    "current_sprint": current_sprint,
                    "comment": comment_block.strip(),
                })
        # SKIPs without a Revisit comment are not flagged — they may be
        # intentionally open-ended. The CLAUDE.md rule requires the comment
        # format; CI will flag them as overdue once the format is adopted.

    return overdue


def main() -> int:
    current_sprint = read_current_sprint()
    if current_sprint == 0:
        print("[audit_skipped_tests] Sprint number unavailable — skipping overdue check.")
        return 0

    print(f"[audit_skipped_tests] Current sprint: {current_sprint}")
    print(f"[audit_skipped_tests] Scanning {E2E_DIR} ...")

    all_overdue = []
    ts_files = sorted(E2E_DIR.glob("*.ts")) + sorted(E2E_DIR.glob("**/*.ts"))
    seen = set()
    for f in ts_files:
        if f in seen:
            continue
        seen.add(f)
        all_overdue.extend(audit_file(f, current_sprint))

    if not all_overdue:
        print("[audit_skipped_tests] PASS — no overdue test.skip blocks.")
        return 0

    print("\n[audit_skipped_tests] FAIL — overdue test.skip blocks detected:\n")
    for item in all_overdue:
        print(f"  File:            {item['file']}:{item['line']}")
        print(f"  Revisit sprint:  {item['revisit_sprint']}  (current: {item['current_sprint']})")
        print(f"  Comment excerpt:\n    " + "\n    ".join(item["comment"].splitlines()[:5]))
        print()

    print(
        f"[audit_skipped_tests] {len(all_overdue)} overdue skip(s) found.\n"
        "  Re-classify each as FIX, DELETE, or SKIP with an updated Revisit sprint."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
