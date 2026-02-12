# TS Functions

## Objective
Implement a pure function that computes an order total from line items.

This quest trains:
- function signatures + return types
- input validation for `unknown`
- deterministic rounding
- clean, test-driven logic

## Requirements
Edit `task.ts` to export:

1) `type LineItem = { sku: string; priceCents: number; qty: number }`
2) `function totalCents(input: unknown): number`

### totalCents rules
Given unknown input, compute the total cost in cents:
- If input is not an array, return 0.
- Each valid line item must have:
  - sku: non-empty string after trim
  - priceCents: integer >= 0
  - qty: integer in range 1..99
- Ignore invalid items (do not throw).

Total is:
`sum(priceCents * qty)` over valid items.

## Constraints
- Standard library only.
- No printing.
- Deterministic behavior.

## Success Criteria
Public tests pass.
