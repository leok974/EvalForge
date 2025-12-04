#!/usr/bin/env python
"""
Register an EvalForge subagent with Antigravity.

Usage:
    python scripts/register_subagent.py \
        [--spec scripts/agents/intent-oracle-evaluator.yaml]

Env:
    ANTIGRAVITY_BASE_URL  (required)
    ANTIGRAVITY_API_TOKEN (required)
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import requests


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--spec",
        default="scripts/agents/intent-oracle-evaluator.yaml",
        help="Path to the subagent spec (YAML or JSON).",
    )
    args = parser.parse_args()

    base_url = os.environ.get("ANTIGRAVITY_BASE_URL")
    token = os.environ.get("ANTIGRAVITY_API_TOKEN")

    if not base_url:
        print("ANTIGRAVITY_BASE_URL is not set", file=sys.stderr)
        return 1
    if not token:
        print("ANTIGRAVITY_API_TOKEN is not set", file=sys.stderr)
        return 1

    spec_path = Path(args.spec)
    if not spec_path.is_file():
        print(f"Spec file not found: {spec_path}", file=sys.stderr)
        return 1

    body = spec_path.read_text(encoding="utf-8")

    # Some Antigravity setups accept YAML directly; if yours expects JSON,
    # you can convert here. For now we send the YAML as-is.
    url = base_url.rstrip("/") + "/api/subagents"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-yaml",
    }

    print(f"→ Registering subagent from {spec_path} at {url}")
    try:
        resp = requests.post(url, data=body.encode("utf-8"), headers=headers, timeout=30.0)
    except requests.RequestException as e:
        print(f"❌ Connection failed: {e}", file=sys.stderr)
        return 1

    print(f"← Status: {resp.status_code}")
    if resp.content:
        print(resp.text)

    if resp.status_code not in (200, 201):
        print("Registration failed", file=sys.stderr)
        return 1

    print("Subagent registration succeeded ✅")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
