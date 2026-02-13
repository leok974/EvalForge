
def verify_output(output: dict, required_keys: list[str]) -> dict:
    missing = [k for k in required_keys if k not in output]
    return {"ok": len(missing) == 0, "missing": missing}
