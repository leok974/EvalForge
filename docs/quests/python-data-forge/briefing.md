# Briefing — Data Forge

## Objective
Read a messy JSON export of contact data, normalize each record to a strict schema, and print the result as a canonical JSON array.

## Where You’ll Work
- Edit: `main.py`
- Input: `fixtures/raw_contacts.json` (do not edit)
- Validation: stdout is checked for deep JSON equality against the expected normalized structure.

## Requirements
- **Input**: List of objects with `id`, `name`, `email`, `phone`, `tags`, `active`.
- **Output**: Canonical JSON string of the normalized list.
- **Normalization**:
  - `id`: Coerce to int.
  - `name`: Title Case, trim whitespace.
  - `email`: Lowercase, trim. Null if empty.
  - `phone`: Format as `XXX-XXX-XXXX` if 10 digits. Null otherwise.
  - `tags`: List of unique, sorted, lowercase strings.
  - `is_active`: Boolean (`true`/`false`).

## Success Criteria
- Output is valid JSON.
- Output exactly matches the expected normalized data (order independent for keys, but list order matters).
- Exit code is 0.
