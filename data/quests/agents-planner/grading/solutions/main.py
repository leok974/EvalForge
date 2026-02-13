
def plan(request: str, tool_names: list[str]) -> list[dict]:
    parts = request.strip().split()
    if not parts:
        return []
    cmd = parts[0].lower()

    if cmd == "add":
        if "add" not in tool_names:
            raise ValueError("NO_TOOL")
        a = int(parts[1]); b = int(parts[2])
        return [{"tool":"add", "args":{"a":a, "b":b}}]

    if cmd == "echo":
        if "echo" not in tool_names:
            raise ValueError("NO_TOOL")
        text = " ".join(parts[1:])
        return [{"tool":"echo", "args":{"text":text}}]

    return []
