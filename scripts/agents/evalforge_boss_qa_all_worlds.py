#!/usr/bin/env python
"""
CLI script to run standard world boss QA pass.
Tests Reactor Core, Signal Prism, and other core world bosses.

Usage:
    python scripts/agents/evalforge_boss_qa_all_worlds.py
    python scripts/agents/evalforge_boss_qa_all_worlds.py --base-url http://localhost:8000
"""
import argparse
import sys
import textwrap
from typing import Any, Dict

import requests


def run_world_boss_qa(base_url: str, session_cookie: str | None = None) -> Dict[str, Any]:
    url = f"{base_url.rstrip('/')}/api/dev/boss_qa/worlds"
    headers = {}
    cookies = {}
    if session_cookie:
        cookies["session"] = session_cookie

    resp = requests.post(url, headers=headers, cookies=cookies, timeout=30)
    resp.raise_for_status()
    return resp.json()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run QA for all standard world bosses (Reactor Core, Signal Prism, etc.).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Examples:

              # Default dev server on port 8081
              python scripts/agents/evalforge_boss_qa_all_worlds.py

              # Custom base URL
              python scripts/agents/evalforge_boss_qa_all_worlds.py --base-url http://localhost:8000

              # With session cookie (if dev API requires auth)
              python scripts/agents/evalforge_boss_qa_all_worlds.py --session-cookie <value>
            """
        ),
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:8081",
        help="Base URL of the EvalForge API (default: http://localhost:8081)",
    )
    parser.add_argument(
        "--session-cookie",
        default=None,
        help="Optional session cookie value if your dev API requires auth.",
    )

    args = parser.parse_args()

    try:
        report = run_world_boss_qa(
            base_url=args.base_url,
            session_cookie=args.session_cookie,
        )
    except Exception as e:
        print(f"[World Boss QA] Request failed: {e}", file=sys.stderr)
        return 1

    overall_pass = report.get("overall_pass", False)
    results = report.get("results", [])

    print("=== EvalForge World Boss QA Report ===")
    print(f"Label: {report.get('label', 'worlds-fundamentals')}")
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
        print("[World Boss QA] FAIL: One or more world bosses did not meet the minimum score.", file=sys.stderr)
        return 1

    print("[World Boss QA] PASS: All standard world bosses meet or exceed the configured thresholds.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
