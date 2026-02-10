# Briefing — React Ignition

## Objective
Edit `task.mjs` to export a React component named **`App`** that renders the welcome UI exactly as required.

## Context
This is the ignition step for the React world: you’ll create a component **without JSX**, using `React.createElement` (the primitive that JSX compiles into). The tests inspect the rendered tree, so structure and text must match exactly.

## Where You’ll Work
- Edit: `data/quests/react-ignition/workspace/task.mjs`
- Tests: `data/quests/react-ignition/grading/public/react-ignition.public.test.mjs`

## Requirements
1. Render a `div` element.
2. The `div` must have a `data-testid="welcome"` prop.
3. The content of the `div` must be **"Hello React"**.
4. Do **not** use JSX. Use `React.createElement`.

## Constraints
- ✅ No JSX (`<div>...</div>` is not allowed)
- ✅ Must use `React.createElement(...)`
- ✅ Exact match for text: `"Hello React"` (case + spacing)

## Success Criteria
- [ ] `App` is exported (named export) from `task.mjs`
- [ ] Rendering `App` produces a `div`
- [ ] `div` is discoverable via `data-testid="welcome"`
- [ ] The first child text equals `"Hello React"`
- [ ] Public tests pass

## How To Verify
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Spec and Codex References

* Spec: `README.md` (this quest)
* Codex: [[codex:react/components]] [[codex:react/jsx]] [[codex:react/props]]
