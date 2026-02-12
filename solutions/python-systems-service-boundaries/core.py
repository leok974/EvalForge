from __future__ import annotations

from typing import Any


def coerce_id(value: Any) -> int:
    """
    Convert string/number ids into an int.
    Examples: "002" -> 2, 1 -> 1
    """
    try:
        return int(str(value).strip())
    except Exception:
        return 0


def _bad(action: str, req_id: Any, code: str) -> dict:
    return {
        "id": coerce_id(req_id),
        "action": action,
        "ok": False,
        "value": None,
        "error": code,
    }


def _ok(action: str, req_id: Any, value: Any) -> dict:
    return {
        "id": coerce_id(req_id),
        "action": action,
        "ok": True,
        "value": value,
        "error": None,
    }


def handle_request(req: dict) -> dict:
    """
    Pure core function: takes a request dict and returns a response dict.

    Must not print, read files, or rely on globals.
    """
    req_id = req.get("id")
    action = req.get("action")
    
    if not isinstance(action, str):
        return _bad(str(action), req_id, "EF_BOUNDARY_UNKNOWN_ACTION")

    if action == "sum":
        numbers = req.get("numbers")
        if not isinstance(numbers, list) or any(not isinstance(x, int) for x in numbers):
            return _bad(action, req_id, "EF_BOUNDARY_BAD_INPUT")
        return _ok(action, req_id, sum(numbers))

    if action == "divide":
        num = req.get("numerator")
        den = req.get("denominator")
        if not isinstance(num, int) or not isinstance(den, int):
            return _bad(action, req_id, "EF_BOUNDARY_BAD_INPUT")
        if den == 0:
            return _bad(action, req_id, "EF_BOUNDARY_DIVIDE_BY_ZERO")
        # Integer division for this quest (per user prompt 'fixture values produce integer result')
        return _ok(action, req_id, num // den)

    if action == "concat":
        parts = req.get("parts")
        if not isinstance(parts, list) or any(not isinstance(x, str) for x in parts):
            return _bad(action, req_id, "EF_BOUNDARY_BAD_INPUT")
        cleaned = [p.strip() for p in parts if p.strip()]
        return _ok(action, req_id, " ".join(cleaned))

    return _bad(action, req_id, "EF_BOUNDARY_UNKNOWN_ACTION")
