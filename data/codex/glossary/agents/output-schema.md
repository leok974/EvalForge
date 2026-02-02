# Output Schema

## Definition
An **output schema** defines the exact structure the assistant must produce (often JSON). It reduces ambiguity and makes responses machine-checkable (for validators, tests, or UI rendering).

## Tiny example
Instead of “Summarize this,” require:
- `{ "bullets": ["...", "...", "..."] }`
with exactly 3 bullets.

## Common pitfall
If you don’t set `additionalProperties: false` (or the equivalent constraint), the assistant may add extra keys. Schemas work best when you strictly define required keys and forbid extras.

## Related
Determinism, Instruction Hierarchy
