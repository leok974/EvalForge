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
    
    # TODO: Implement request handling logic
    # 1. Validate action and inputs
    # 2. Return _ok or _bad response
    
    return _bad(str(action), req_id, "EF_BOUNDARY_NOT_IMPLEMENTED")
