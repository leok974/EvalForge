# Briefing — TS Modules

## Objective
Build a two-file module system:
- `math.ts` exports helpers
- `task.ts` imports helpers and formats the invoice total

## Contract
- `sum([]) => 0`
- `toCents(dollars) => Math.round(dollars * 100)`
- `formatInvoiceTotal([...]) => "Total: <cents> cents"`

## Success Criteria
Public tests pass with no extra output.
