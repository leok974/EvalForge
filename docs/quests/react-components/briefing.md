# Briefing — React Components: Composition

## Objective
Implement **two components** in `task.mjs` — `Card` and `CardBody` — so they render a composed structure exactly as specified.

## Context
This quest teaches **component composition**: one component rendering another as a child. You’re practicing how React elements nest and how test IDs help verify structure.

## Where You’ll Work
- Edit: `data/quests/react-components/workspace/task.mjs`
- Tests: `data/quests/react-components/grading/public/react-components.public.test.mjs`

## Requirements
1. `CardBody` renders a `div` with `data-testid="card-body"` and text **"I am the body"**.
2. `Card` renders a `div` with `data-testid="card"`.
3. `Card` renders `CardBody` **nested inside** the card div.

Target structure:
```html
<div data-testid="card">
  <div data-testid="card-body">I am the body</div>
</div>
```

## Constraints

* ✅ No JSX — use `React.createElement`
* ✅ `CardBody` must be inside `Card` (nesting matters)

## Success Criteria

* [ ] `CardBody` returns a `div` with test id `card-body` and the exact text
* [ ] `Card` returns a `div` with test id `card`
* [ ] `Card` renders `CardBody` as a child (nested)
* [ ] Public tests pass

## How To Verify

```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Spec and Codex References

* Spec: `README.md` (this quest)
* Codex: [[codex:react/components]] [[codex:react/props]] [[codex:react/jsx]]
