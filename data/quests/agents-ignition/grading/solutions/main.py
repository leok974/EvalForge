
def _collapse_ws(s: str) -> str:
    return " ".join(s.strip().split())

def format_prompt(system: str, user: str) -> str:
    system = system.strip()
    user = _collapse_ws(user)
    return f"SYSTEM: {system}\nUSER: {user}"
