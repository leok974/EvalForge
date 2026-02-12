# Tutorial — TS Modules

## What You’re Practicing
- Named exports: `export function ...`
- Imports: `import { x } from "./file.ts"`
- Keeping logic in the correct module

## Implementation Plan
1. Implement `sum` in `math.ts`.
2. Implement `toCents` in `math.ts` using `Math.round(dollars * 100)`.
3. In `task.ts`, map line totals through `toCents`, then sum with `sum`.
4. Return `Total: <cents> cents`.

## Pitfalls
- Forgetting to export functions in `math.ts`
- Import path mistakes (`./math.ts` vs `math.ts`)
- Using `Math.floor` instead of `Math.round`
