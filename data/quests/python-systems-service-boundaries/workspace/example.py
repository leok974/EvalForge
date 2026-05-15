def coerce_id(value) -> int:
    try:
        return int(str(value).strip())
    except Exception:
        return 0


def _bad(action, req_id, code):
    return {"id": coerce_id(req_id), "action": action, "ok": False, "value": None, "error": code}


def _ok(action, req_id, value):
    return {"id": coerce_id(req_id), "action": action, "ok": True, "value": value, "error": None}


def handle_request(req: dict) -> dict:
    req_id = req.get("id")
    action = req.get("action")
    args = req.get("args", [])

    if action == "divide":
        if len(args) < 2 or args[1] == 0:
            return _bad(action, req_id, "EF_BOUNDARY_DIVIDE_BY_ZERO")
        return _ok(action, req_id, args[0] // args[1])
    if action == "sum":
        if not all(isinstance(a, (int, float)) for a in args):
            return _bad(action, req_id, "EF_BOUNDARY_BAD_INPUT")
        return _ok(action, req_id, sum(args))
    if action == "concat":
        return _ok(action, req_id, "".join(str(a) for a in args))
    return _bad(action, req_id, "EF_BOUNDARY_UNKNOWN_ACTION")
