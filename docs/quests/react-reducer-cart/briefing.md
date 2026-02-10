# Briefing — React Reducer: Shopping Cart

## Objective
Implement `ShoppingCart` using `useReducer` so it can add 10 to a total and reset to 0.

## Context
`useReducer` is state management with explicit actions:
action in → reducer computes next state → UI renders state.
This quest drills predictable updates via action objects.

## Where You’ll Work
- Edit: `data/quests/react-reducer-cart/workspace/task.mjs`
- Tests: `data/quests/react-reducer-cart/grading/public/react-reducer-cart.public.test.mjs`

## Requirements
1. Use `useReducer`. Initial state: `{ total: 0 }`.
2. Render `div[data-testid="total"]` showing current total.
3. Render `button[data-testid="add-10"]` that adds 10.
4. Render `button[data-testid="reset"]` that resets to 0.
5. Actions roughly: `{ type: "ADD", amount: 10 }` and `{ type: "RESET" }`.

## Constraints
- ✅ No JSX — use `React.createElement`
- ✅ Reducer must return new state objects (don’t mutate)

## Success Criteria
- [ ] Total renders as `"0"` initially
- [ ] Clicking add-10 twice shows `"10"` then `"20"`
- [ ] Reset returns total to `"0"` (likely hidden test)
- [ ] Public tests pass

## How To Verify
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Spec and Codex References

* Spec: `README.md` (this quest)
* Codex: [[codex:react/state]] [[codex:react/events]] [[codex:react/components]]
