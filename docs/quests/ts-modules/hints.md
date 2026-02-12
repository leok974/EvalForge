# Hints — TS Modules

## Hint 1
The import must be relative:
`import { sum, toCents } from "./math.ts"`

## Hint 2
Convert dollars → cents first, then sum.

## Hint 3
Rounding matters: `Math.round(1.005 * 100) === 101`.
