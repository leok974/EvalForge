from __future__ import annotations

import re


def slugify(text: str) -> str:
    """Convert text to a URL-safe slug.

    Steps:
      1. Lowercase and strip leading/trailing whitespace.
      2. Replace spaces with dashes.
      3. Remove characters that are not a-z, 0-9, or dash.
      4. Collapse consecutive dashes into one dash.
      5. Strip any remaining leading/trailing dashes.
    """
    raise NotImplementedError("TODO: implement slugify(text)")


def unique_sorted(items: list[str]) -> list[str]:
    """Return a deduplicated, alphabetically sorted list.

    For each item:
      - Strip leading/trailing whitespace.
      - Lowercase.
      - Drop empty strings.
    Deduplicate and sort the result.
    """
    raise NotImplementedError("TODO: implement unique_sorted(items)")


def _bad(tool: str, code: str) -> dict:
    return {"tool": tool, "ok": False, "result": None, "error": code}


def _ok(tool: str, result) -> dict:
    return {"tool": tool, "ok": True, "result": result, "error": None}


def run_tool_request(req: dict) -> dict:
    """Dispatch a tool request to the correct handler.

    req = {"tool": "<name>", "payload": {...}}

    Supported tools and their payload keys:
      "slugify"       → payload["text"]    (str)
      "sum"           → payload["numbers"] (list[int])
      "unique_sorted" → payload["items"]   (list[str])

    Return _ok(tool, result) on success.
    Return _bad(tool, "EF_TOOL_UNKNOWN") for unrecognised tool names.
    Return _bad(tool, "EF_TOOL_BAD_INPUT") for missing/wrong-type payloads
    or an empty/missing tool name.
    """
    raise NotImplementedError("TODO: implement run_tool_request(req)")
