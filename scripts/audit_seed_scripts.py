#!/usr/bin/env python3
"""
audit_seed_scripts.py — Enforce the "seed scripts must upsert" rule.

Scans scripts/*seed*.py for INSERT-only patterns.  A seed script is safe
when it either (a) queries for existing records before adding, or (b) uses
an ON CONFLICT / on_conflict_do_update clause.  A script that only calls
session.add() without any existence check will silently duplicate rows on
re-runs.

Exit 0 — all seed scripts are safe.
Exit 1 — at least one seed script looks insert-only.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"

# Matches a positively-identified upsert or existence check.
UPSERT_RE = re.compile(
    r"select\(|\.exec\(|on_conflict|ON CONFLICT|merge_|\.merge\(|get_or_create|"
    r"session\.get\(|\.first\(\)|\.one_or_none\(\)|\.scalars\(\)|\.scalar\(\)",
    re.IGNORECASE,
)

# Matches any insert action.
INSERT_RE = re.compile(
    r"session\.add\(|INSERT INTO|\.add_all\(",
    re.IGNORECASE,
)

# Scripts that are explicitly whitelisted (one-time-only by design, documented).
WHITELIST: set[str] = set()


def audit_script(path: Path) -> str | None:
    """Return an error string if the script looks insert-only, else None."""
    if path.name in WHITELIST:
        return None

    text = path.read_text(encoding="utf-8", errors="replace")

    has_insert = bool(INSERT_RE.search(text))
    has_upsert = bool(UPSERT_RE.search(text))

    if has_insert and not has_upsert:
        return f"  {path.name}: session.add() / INSERT found but no existence check or ON CONFLICT."

    return None


def main() -> int:
    seed_scripts = sorted(SCRIPTS_DIR.glob("*seed*.py"))
    if not seed_scripts:
        print("[audit_seed_scripts] No seed scripts found — nothing to check.")
        return 0

    failures: list[str] = []
    for path in seed_scripts:
        err = audit_script(path)
        if err:
            failures.append(err)

    if not failures:
        print(f"[audit_seed_scripts] PASS — all {len(seed_scripts)} seed scripts have upsert patterns.")
        return 0

    print("[audit_seed_scripts] FAIL — insert-only seed scripts detected:\n")
    for msg in failures:
        print(msg)
    print(
        "\nEach flagged script must either:\n"
        "  1. Query for an existing record before calling session.add(), or\n"
        "  2. Use ON CONFLICT / on_conflict_do_update for bulk inserts.\n"
        "If the script is intentionally one-shot (documented), add its filename\n"
        "to the WHITELIST set in audit_seed_scripts.py."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
