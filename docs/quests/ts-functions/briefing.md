# Briefing — TS Functions

## Objective
Compute an order total from a list of line items, safely and deterministically.

## Contract
- Non-array input → 0
- Validate each item:
  - sku: non-empty string after trim
  - priceCents: integer ≥ 0
  - qty: integer 1..99
- Ignore invalid items
- Return sum(priceCents * qty)

## Success Criteria
Public tests pass with no extra output.
