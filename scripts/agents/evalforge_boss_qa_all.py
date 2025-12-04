#!/usr/bin/env python
"""
Unified CLI script to run QA for ALL bosses (world + project bosses).
Tests both standard world bosses and ApplyLens project bosses in one pass.

Usage:
    python scripts/agents/evalforge_boss_qa_all.py
    python scripts/agents/evalforge_boss_qa_all.py --runtime-min 75 --agent-min 75
"""
import argparse
import sys
import textwrap
from typing import Any, Dict

import requests


def _post_json(
    url: str,
    params: Dict[str, Any] | None = None,
    session_cookie: str | None = None,
    timeout: int = 30,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    cookies: Dict[str, str] = {}
    if session_cookie:
        cookies["session"] = session_cookie

    resp = requests.post(url, params=params or {}, headers=headers, cookies=cookies, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def run_world_boss_qa(base_url: str, session_cookie: str | None = None) -> Dict[str, Any]:
    url = f"{base_url.rstrip('/')}/api/dev/boss_qa/worlds"
    return _post_json(url, session_cookie=session_cookie)


def run_applylens_boss_qa(
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
    return _post_json(url, params=params, session_cookie=session_cookie)


def print_world_report(report: Dict[str, Any]) -> None:
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


def print_applylens_report(report: Dict[str, Any]) -> None:
    overall_pass = report.get("overall_pass", False)
    results = report.get("results", [])

    print("=== ApplyLens Project Boss QA Report ===")
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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run QA for ALL bosses (world bosses + ApplyLens project bosses).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Examples:

              # Default dev server on port 8081, default thresholds
              python scripts/agents/evalforge_boss_qa_all.py

              # Custom base URL
              python scripts/agents/evalforge_boss_qa_all.py --base-url http://localhost:8000

              # Stricter project boss thresholds
              python scripts/agents/evalforge_boss_qa_all.py --runtime-min 75 --agent-min 75

              # With session cookie (if dev API requires auth)
              python scripts/agents/evalforge_boss_qa_all.py --session-cookie <value>
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
        help="Minimum score required for the ApplyLens runtime boss (default: 60)",
    )
    parser.add_argument(
        "--agent-min",
        type=int,
        default=60,
        help="Minimum score required for the ApplyLens agent boss (default: 60)",
    )
    parser.add_argument(
        "--session-cookie",
        default=None,
        help="Optional session cookie value if your dev API requires auth.",
    )
    parser.add_argument(
        "--worlds-only",
        action="store_true",
        help="Only run QA for standard world bosses (skip ApplyLens bosses).",
    )
    parser.add_argument(
        "--projects-only",
        action="store_true",
        help="Only run QA for project bosses (ApplyLens), skip world bosses.",
    )

    args = parser.parse_args()

    base_url = args.base_url
    session_cookie = args.session_cookie

    any_fail = False

    # Worlds
    if not args.projects_only:
        try:
            world_report = run_world_boss_qa(
                base_url=base_url,
                session_cookie=session_cookie,
            )
            print_world_report(world_report)
            if not world_report.get("overall_pass", False):
                any_fail = True
        except Exception as e:
            print(f"[World Boss QA] Request failed: {e}", file=sys.stderr)
            return 1

    # ApplyLens project bosses
    if not args.worlds_only:
        try:
            applylens_report = run_applylens_boss_qa(
                base_url=base_url,
                min_score_runtime=args.runtime_min,
                min_score_agent=args.agent_min,
                session_cookie=session_cookie,
            )
            print_applylens_report(applylens_report)
            if not applylens_report.get("overall_pass", False):
                any_fail = True
        except Exception as e:
            print(f"[ApplyLens Boss QA] Request failed: {e}", file=sys.stderr)
            return 1

    if any_fail:
        print("[Boss QA] FAIL: One or more bosses did not meet the minimum score.", file=sys.stderr)
        return 1

    print("[Boss QA] PASS: All bosses (world + project) meet or exceed the configured thresholds.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
