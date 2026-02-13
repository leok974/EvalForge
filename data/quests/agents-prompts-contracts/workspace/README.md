# Prompt Contracts

Implement `validate_prompt_contract(contract)` returning a list of error strings.

Contract must contain:
- system: non-empty str
- user: non-empty str
- tools: list[str]
- max_tokens: int > 0
Return [] if valid.
