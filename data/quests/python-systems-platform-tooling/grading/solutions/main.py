from __future__ import annotations

import re


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = text.replace(" ", "-")
    text = re.sub(r"[^a-z0-9-]", "", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def unique_sorted(items: list[str]) -> list[str]:
    return sorted({s.lower().strip() for s in items if s.strip()})


def _bad(tool: str, code: str) -> dict:
    return {"tool": tool, "ok": False, "result": None, "error": code}


def _ok(tool: str, result) -> dict:
    return {"tool": tool, "ok": True, "result": result, "error": None}


def run_tool_request(req: dict) -> dict:
    tool = req.get("tool", "")
    payload = req.get("payload", {})
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
