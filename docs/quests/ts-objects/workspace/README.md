# TS Objects

## Objective
Normalize a partial configuration object into a complete config with defaults.

This quest trains:
- object types
- optional properties
- safe merging with defaults
- deterministic output

## Requirements
Edit `task.ts` to export:

1) `type Config`
2) `function normalizeConfig(input: unknown): Config`

### Config shape
`Config` must be:
- `retries`: number (0..10)
- `timeoutMs`: number (50..5000)
- `baseUrl`: string (non-empty)
- `headers`: Record<string, string> (lowercased keys)

### Defaults
If input is invalid or missing fields, use defaults:
- retries: 3
- timeoutMs: 500
- baseUrl: "https://api.local"
- headers: { "x-client": "evalforge" }

### Normalization rules
Given `input`:
- If input is not a plain object, treat it as empty.
- `retries`:
  - accept integer numbers only
  - clamp to 0..10
- `timeoutMs`:
  - accept integer numbers only
  - clamp to 50..5000
- `baseUrl`:
  - accept non-empty string after trim, else default
- `headers`:
  - accept a plain object of string→string
  - trim values
  - lowercase keys
  - drop entries with empty key or empty value

## Output
Return the normalized `Config` object (do not print).

## Constraints
- Standard library only.
- No IO.
- Deterministic behavior.

## Success Criteria
Public tests pass.
