"""
Quest: python-systems-platform-tooling

Implement three pure utility functions that form the backbone of an internal
developer toolbox. No I/O: inputs come in, results come out.

Functions to implement (in main.py):

  slugify(text: str) -> str
    Convert text to a URL-safe slug:
      1. Lowercase and strip.
      2. Replace spaces with dashes.
      3. Remove non-alphanumeric characters (except dashes).
      4. Collapse consecutive dashes.
      5. Strip leading/trailing dashes.

  unique_sorted(items: list[str]) -> list[str]
    Return a deduplicated, alphabetically sorted list of stripped,
    lowercased, non-empty strings.

  run_tool_request(req: dict) -> dict
    Dispatch {"tool": "<name>", "payload": {...}} to the matching function.
    Supported tools: "slugify", "sum", "unique_sorted".
    Return {"tool": ..., "ok": True/False, "result": ..., "error": ...}.
    Error codes: "EF_TOOL_UNKNOWN", "EF_TOOL_BAD_INPUT".

Edit main.py — the grader imports from there.
"""
