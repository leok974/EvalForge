
def validate_prompt_contract(contract: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(contract, dict):
        return ["contract_not_dict"]

    def need_str(k: str):
        v = contract.get(k)
        if not isinstance(v, str) or not v.strip():
            errors.append(f"{k}_invalid")

    need_str("system")
    need_str("user")

    tools = contract.get("tools")
    if not isinstance(tools, list) or not all(isinstance(t, str) for t in tools):
        errors.append("tools_invalid")

    mt = contract.get("max_tokens")
    if not isinstance(mt, int) or mt <= 0:
        errors.append("max_tokens_invalid")

    return errors
