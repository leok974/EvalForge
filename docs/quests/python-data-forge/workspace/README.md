# Data Forge

## Objective
Read a messy JSON export from `fixtures/raw_contacts.json`, normalize each record, and print a canonical JSON array to stdout.

## Input
A JSON array of objects in `fixtures/raw_contacts.json`.

## Output
Print exactly one line: the normalized JSON array using canonical formatting:
`json.dumps(out, sort_keys=True, separators=(",",":"))`

## Normalization Rules
- id → int
- name → trim, collapse spaces, Title Case; missing/empty/null → "Unknown"
- email → trim + lowercase; empty/missing/null → null
- phone → digits-only; if 10 digits format XXX-XXX-XXXX else null
- tags → list; string splits on commas; lowercase, trim, drop empty; unique + sorted; missing/null → []
- is_active → boolean from common truthy/falsey inputs; missing/null → false

## Determinism
- Output list sorted by id ascending.
- No extra stdout beyond the JSON line.
