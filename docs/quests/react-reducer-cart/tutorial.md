# Tutorial — React Reducer: Shopping Cart

## What You’ll Learn
- How `useReducer` replaces `useState` for action-driven updates
- Writing a reducer that handles multiple action types
- Dispatching actions from button click handlers

## Approach
Treat the reducer as the “single source of truth” for how totals change:
- ADD action increases `total` by `amount`
- RESET action returns `{ total: 0 }`

Render `String(state.total)` so text comparisons match the tests.

## Implementation Plan
1. Implement the reducer:
   - `ADD` → `{ total: state.total + action.amount }`
   - `RESET` → `{ total: 0 }`
   - default → `state`
2. Wire button handlers:
   - add-10 button dispatches `{ type: "ADD", amount: 10 }`
   - reset button dispatches `{ type: "RESET" }`
3. Render total:
   - `div[data-testid="total"]` with `String(state.total)`

## Testing
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Pitfalls

* Returning the same state for ADD (no updates)
* Mutating `state.total` instead of returning a new object
* Forgetting `onClick` handlers
* Rendering a number that your test renderer exposes as non-string

## Self-Check

* Start: `"0"`
* Click add-10: `"10"`
* Click add-10 again: `"20"`
* Click reset: `"0"`
