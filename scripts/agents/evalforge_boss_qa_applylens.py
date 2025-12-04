#!/usr/bin/env python
"""
CLI script to run ApplyLens boss QA pass.
Tests both Inbox Maelstrom and Intent Oracle using ZERO + rubrics.

Usage:
    python scripts/agents/evalforge_boss_qa_applylens.py
    python scripts/agents/evalforge_boss_qa_applylens.py --runtime-min 75 --agent-min 75
"""
import argparse
import sys
import textwrap
from typing import Any, Dict

import requests


def run_boss_qa(
    base_url: str,
    min_score_runtime: int,
    min_score_agent: int,
    session_cookie: str | None = None,
) -> Dict[str, Any]:
    url = f"{base_url.rstrip('/')}/api/dev/boss_qa/applylens"
    params = {
        "min_score_runtime": min_score_runtime,
        "min_score_agent": min_score_agent,
    }

    headers = {}
    cookies = {}
    if session_cookie:
        cookies["session"] = session_cookie

    resp = requests.post(url, params=params, headers=headers, cookies=cookies, timeout=30)
    resp.raise_for_status()
    return resp.json()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a full boss QA pass for ApplyLens (Inbox Maelstrom + Intent Oracle).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Examples:

              # Default dev server on port 8081, default score thresholds
              python scripts/agents/evalforge_boss_qa_applylens.py

              # Custom base URL
              python scripts/agents/evalforge_boss_qa_applylens.py --base-url http://localhost:8000

              # Stricter thresholds
              python scripts/agents/evalforge_boss_qa_applylens.py --runtime-min 75 --agent-min 75
            """
        ),
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:8081",
        help="Base URL of the EvalForge API (default: http://localhost:8081)",
    )
    parser.add_argument(
        "--runtime-min",
        type=int,
        default=60,
        help="Minimum score required for the runtime boss to pass (default: 60)",
    )
    parser.add_argument(
        "--agent-min",
        type=int,
        default=60,
        help="Minimum score required for the agent boss to pass (default: 60)",
    )
    parser.add_argument(
        "--session-cookie",
        default=None,
        help="Optional session cookie value if your dev API requires auth.",
    )

    args = parser.parse_args()

    try:
        report = run_boss_qa(
            base_url=args.base_url,
            min_score_runtime=args.runtime_min,
            min_score_agent=args.agent_min,
            session_cookie=args.session_cookie,
        )
    except Exception as e:
        print(f"[Boss QA] Request failed: {e}", file=sys.stderr)
        return 1

    overall_pass = report.get("overall_pass", False)
    results = report.get("results", [])

    print("=== ApplyLens Boss QA Report ===")
    print(f"Project: {report.get('project_slug', 'applylens')}")
    print(f"Overall pass: {overall_pass}")
    print()

    for r in results:
        print(f"- Boss: {r.get('boss_slug')}")
        print(f"  Rubric: {r.get('rubric_id')}")
        print(f"  Score: {r.get('score')} / {r.get('min_score_required')} (grade {r.get('grade')})")
        print(f"  Passed: {r.get('passed')}")
        print(f"  Boss HP: {r.get('boss_hp_before')} → {r.get('boss_hp_after')} ({r.get('boss_hp_delta')})")
        print(
            f"  Integrity: {r.get('integrity_before')} → {r.get('integrity_after')} "
            f"({r.get('integrity_delta')})"
        )
        print()

    if not overall_pass:
        print("[Boss QA] FAIL: One or more bosses did not meet the minimum score.", file=sys.stderr)
        return 1

    print("[Boss QA] PASS: All ApplyLens bosses meet or exceed the configured thresholds.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
