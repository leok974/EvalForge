# Briefing — React State: Toggle

## Objective
Implement `ToggleButton` so it toggles between `"OFF"` and `"ON"` when clicked.

## Context
This is state + events in the smallest possible loop:
state drives text → click flips state → UI updates.

## Where You’ll Work
- Edit: `data/quests/react-state-toggle/workspace/task.mjs`
- Tests: `data/quests/react-state-toggle/grading/public/react-state-toggle.public.test.mjs`

## Requirements
1. Render a `button` with `data-testid="toggle"`.
2. Initial text is `"OFF"`.
3. On click, swap between `"OFF"` and `"ON"`.

## Constraints
- ✅ No JSX — use `React.createElement`
- ✅ Text must match exactly

## Success Criteria
- [ ] Initial render shows `"OFF"`
- [ ] Click once → `"ON"`
- [ ] Click again → `"OFF"`
- [ ] Public tests pass

## How To Verify
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Spec and Codex References

* Spec: `README.md` (this quest)
* Codex: [[codex:react/state]] [[codex:react/events]] [[codex:react/components]]
