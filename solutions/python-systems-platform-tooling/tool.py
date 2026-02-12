from __future__ import annotations

import re
from typing import Any


def _bad(tool: str, code: str) -> dict:
    return {"tool": tool, "ok": False, "result": None, "error": code}


def _ok(tool: str, result: Any) -> dict:
    return {"tool": tool, "ok": True, "result": result, "error": None}


def slugify(text: str) -> str:
    """
    Rules:
    - lowercase
    - trim
    - collapse whitespace to single spaces
    - spaces -> "-"
    - remove all chars except a-z, 0-9, "-"
    - collapse multiple "-" to one
    - strip leading/trailing "-"
    """
    s = text.lower().strip()
    # collapse internal whitespace to single spaces
    s = re.sub(r"\s+", " ", s)
    # spaces -> "-"
    s = s.replace(" ", "-")
    # remove all chars except a-z, 0-9, "-"
    s = re.sub(r"[^a-z0-9-]", "", s)
    # collapse multiple "-" to one
    s = re.sub(r"-+", "-", s)
    # strip leading/trailing "-"
    s = s.strip("-")
    return s


def unique_sorted(items: list[str]) -> list[str]:
    """
    - trim, lowercase
    - drop empty
    - unique + sorted
    """
    cleaned = set()
    for item in items:
        s = item.strip().lower()
        if s:
            cleaned.add(s)
    return sorted(list(cleaned))


def run_tool_request(req: dict) -> dict:
    """
    Pure function: no IO.
    """
    tool = req.get("tool")
    payload = req.get("payload")

    if not isinstance(tool, str) or not tool.strip():
        return _bad("unknown", "EF_TOOL_BAD_INPUT")

    tool = tool.strip()

    if not isinstance(payload, dict):
        return _bad(tool, "EF_TOOL_BAD_INPUT")

    if tool == "slugify":
        text = payload.get("text")
        if not isinstance(text, str):
            return _bad(tool, "EF_TOOL_BAD_INPUT")
        return _ok(tool, slugify(text))

    if tool == "sum":
        nums = payload.get("numbers")
        if not isinstance(nums, list) or any(not isinstance(n, int) for n in nums):
            return _bad(tool, "EF_TOOL_BAD_INPUT")
        return _ok(tool, sum(nums))

    if tool == "unique_sorted":
        items = payload.get("items")
        if not isinstance(items, list) or any(not isinstance(x, str) for x in items):
            return _bad(tool, "EF_TOOL_BAD_INPUT")
        return _ok(tool, unique_sorted(items))

    return _bad(tool, "EF_TOOL_UNKNOWN")
