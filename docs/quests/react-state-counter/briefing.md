# Briefing — React State: Counter

## Objective
Implement a `Counter` component using `useState` that increments and resets a count.

## Context
State is memory inside a component. This quest drills:
- initializing state
- updating state via event handlers
- re-rendering with the new state

## Where You’ll Work
- Edit: `data/quests/react-state-counter/workspace/task.mjs`
- Tests: `data/quests/react-state-counter/grading/public/react-state-counter.public.test.mjs`

## Requirements
1. Render `div[data-testid="count"]` showing the current count (starts at 0).
2. Render `button[data-testid="increment"]` that adds 1.
3. Render `button[data-testid="reset"]` that resets count to 0.
4. Use `React.useState`.

## Constraints
- ✅ No JSX — use `React.createElement`
- ✅ Wire `onClick` handlers for both buttons
- ✅ Count text should match the tests (string output)

## Success Criteria
- [ ] Count starts at `"0"`
- [ ] Clicking increment updates to `"1"`, `"2"`, ...
- [ ] Clicking reset returns to `"0"` (often checked by hidden tests)
- [ ] Public tests pass

## How To Verify
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Spec and Codex References

* Spec: `README.md` (this quest)
* Codex: [[codex:react/state]] [[codex:react/events]] [[codex:react/components]]
