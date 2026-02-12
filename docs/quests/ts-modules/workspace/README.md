# TS Modules

## Objective
Practice TypeScript modules by importing functions from another file.

This quest trains:
- named exports
- importing from relative paths
- building a small module boundary

## Requirements
You must use two files:

### 1) math.ts
Export these named functions:
- `sum(nums: number[]): number`
- `toCents(dollars: number): number`

Rules:
- `sum` returns the total of the numbers (empty array => 0)
- `toCents` converts dollars to cents using rounding:
  `Math.round(dollars * 100)`

### 2) task.ts
Import `sum` and `toCents` from `math.ts`.

Export:
- `function formatInvoiceTotal(lineTotalsDollars: number[]): string`

Rules:
- Convert each line total (dollars) to cents using `toCents`
- Sum cents using `sum`
- Return string: `Total: <cents> cents`
Example: `Total: 4250 cents`

## Constraints
- Standard library only.
- No printing.
- Deterministic behavior.

## Success Criteria
Public tests pass.
