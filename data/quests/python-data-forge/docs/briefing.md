# Briefing: Data Forge

## The Mission
Reactor Core's intake buffers are being flooded with "junk telemetry" from the old manufacturing sector. The data is theoretically valid JSON, but the field names are inconsistent, and data types are all over the place.

Your mission is to build a **normalization pipeline** that takes these raw records and converts them into a stable, canonical format.

## Objectives
- Read raw records from `fixtures/raw_contacts.json`.
- Normalize each record:
  - `id`: Convert to `int`.
  - `name`: Clean whitespace, default to "Unknown" if missing.
  - `email`: Convert to lowercase, default to `null` if invalid/missing.
  - `is_active`: Coerce to `bool`.
  - `tags`: Ensure it's a list (split string by comma if necessary).
- Sort the final list by `id` in ascending order.
- Output the resulting list as a JSON string to stdout.

## Constraints
- Do not use external libraries like `pandas` or `pydantic` (keep it lightweight!).
- Use standard Python `json` and `pathlib` modules.
