#!/usr/bin/env python3
"""
pre-push hook — cherry-pick deletion guard.

For every commit being pushed that is not already on the remote, runs
check_cherry_pick_diff.py and fails the push if any symbol deletions are
detected without explicit confirmation.

Git passes push refs via stdin in the format:
    <local-ref> <local-sha1> <remote-ref> <remote-sha1>

A SHA of 0000000000000000000000000000000000000000 means the branch is
being deleted (remote-sha1) or is a new branch (local-sha1 for new branch).

To bypass in emergencies (documented deletions):
    git push --no-verify
"""

import subprocess
import sys
from pathlib import Path

ZERO_SHA = "0" * 40
REPO_ROOT = Path(__file__).resolve().parent.parent.parent  # .git/hooks -> repo root
GUARD_SCRIPT = REPO_ROOT / "scripts" / "check_cherry_pick_diff.py"


def commits_to_check(local_sha: str, remote_sha: str) -> list[str]:
    """
    Return the list of commit SHAs that are in local_sha but not remote_sha.
    These are the commits about to be pushed for the first time.
    """
    if local_sha == ZERO_SHA:
        return []  # branch deletion — nothing to check

    if remote_sha == ZERO_SHA:
        # New branch — check all commits not reachable from any remote
        result = subprocess.run(
            ["git", "rev-list", local_sha, "--not", "--remotes"],
            capture_output=True, text=True,
        )
    else:
        result = subprocess.run(
            ["git", "rev-list", f"{remote_sha}..{local_sha}"],
            capture_output=True, text=True,
        )

    if result.returncode != 0:
        return []
    return [sha.strip() for sha in result.stdout.splitlines() if sha.strip()]


def main() -> int:
    if not GUARD_SCRIPT.exists():
        print(f"[pre-push] WARNING: guard script not found at {GUARD_SCRIPT}", file=sys.stderr)
        print("[pre-push] Skipping deletion check — push allowed.", file=sys.stderr)
        return 0

    flagged: list[tuple[str, str]] = []  # (sha, output) pairs with deletions

    for line in sys.stdin:
        parts = line.strip().split()
        if len(parts) != 4:
            continue
        _local_ref, local_sha, _remote_ref, remote_sha = parts

        for sha in commits_to_check(local_sha, remote_sha):
            result = subprocess.run(
                [sys.executable, str(GUARD_SCRIPT), sha],
                capture_output=True, text=True,
            )
            if result.returncode == 1:
                flagged.append((sha, result.stdout.strip()))

    if not flagged:
        return 0

    print("\n[pre-push] BLOCKED — cherry-pick guard detected deletions:\n", file=sys.stderr)
    for sha, output in flagged:
        print(f"  Commit {sha}:", file=sys.stderr)
        for l in output.splitlines():
            print(f"    {l}", file=sys.stderr)
        print(file=sys.stderr)

    print(
        "[pre-push] If these deletions are intentional, document them in the\n"
        "           commit message, then re-push with:\n"
        "               git push --no-verify\n",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
