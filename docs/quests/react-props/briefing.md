# Briefing — React Props: Dynamic Greeting

## Objective
Implement a `Welcome` component that renders a greeting based on the `name` prop.

## Context
Props are how data flows **into** components. This quest drills: “read props → render text deterministically.”

## Where You’ll Work
- Edit: `data/quests/react-props/workspace/task.mjs`
- Tests: `data/quests/react-props/grading/public/react-props.public.test.mjs`

## Requirements
1. Accept a prop `name`.
2. Render an `h1` with `data-testid="welcome"`.
3. If `name` is provided, text: `Hello, {name}!`
4. If `name` is missing (`undefined`/`null`), text: `Hello, Stranger!`

## Constraints
- ✅ No JSX — use `React.createElement`
- ✅ Treat only `null`/`undefined` as “missing” (not empty string)

## Success Criteria
- [ ] `Welcome` is exported
- [ ] Renders `h1[data-testid="welcome"]`
- [ ] Correct text when `name` is present
- [ ] Correct fallback when `name` is missing
- [ ] Public tests pass

## How To Verify
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Spec and Codex References

* Spec: `README.md` (this quest)
* Codex: [[codex:react/props]] [[codex:react/components]] [[codex:react/jsx]]
