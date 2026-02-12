# TS Control

## Objective
Implement a typed decision function that classifies HTTP-like status codes.

This quest trains:
- control flow (`if` / `else`)
- boundary handling
- returning exact string literal unions
- defensive programming (invalid inputs)

## Requirements
Edit `task.ts` to export:

1) `type StatusClass = "success" | "redirect" | "client_error" | "server_error" | "invalid"`
2) `function classifyStatus(code: unknown): StatusClass`

### classifyStatus rules
- If `code` is not a number, return `"invalid"`.
- If `code` is not an integer, return `"invalid"`.
- If `code` is < 100 or > 599, return `"invalid"`.

Otherwise:
- 200–299 → `"success"`
- 300–399 → `"redirect"`
- 400–499 → `"client_error"`
- 500–599 → `"server_error"`
- Anything else (100–199) → `"invalid"` (not classified for this quest)

## Constraints
- Standard library only.
- No printing.
- Deterministic behavior.

## Success Criteria
Public tests pass.
