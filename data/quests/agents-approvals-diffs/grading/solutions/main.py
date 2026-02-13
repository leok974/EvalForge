
def apply_diff(base: str, diff: list[dict], approved: bool) -> str:
    if not approved:
        raise PermissionError("NOT_APPROVED")
    s = base
    offset = 0
    for e in diff:
        start = int(e["start"]) + offset
        end = int(e["end"]) + offset
        text = str(e["text"])
        s = s[:start] + text + s[end:]
        offset += len(text) - (end - start)
    return s
