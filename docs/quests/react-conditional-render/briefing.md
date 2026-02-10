# Briefing — React Conditional Render

## Objective
Implement `ToggleSection` so it conditionally renders content based on `isVisible`, while always rendering the title.

## Context
Conditional rendering is a core React skill: decide what appears in the element tree based on state/props.

## Where You’ll Work
- Edit: `data/quests/react-conditional-render/workspace/task.mjs`
- Tests: `data/quests/react-conditional-render/grading/public/react-conditional-render.public.test.mjs`

## Requirements
1. Accept props `title` (string) and `isVisible` (boolean).
2. Always render an `h2` with the `title`.
3. If `isVisible` is true, render a `p` tag with text **"Now you see me"**.
4. If `isVisible` is false, do **NOT** render the `p` tag.

## Constraints
- ✅ No JSX — use `React.createElement`
- ✅ When hidden, the `p` element must not exist in the tree (not empty text)

## Success Criteria
- [ ] `h2` renders the title always
- [ ] `p` renders only when visible
- [ ] Hidden mode produces no `p` element
- [ ] Public tests pass (and hidden behavior likely covered by hidden tests)

## How To Verify
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Spec and Codex References

* Spec: `README.md` (this quest)
* Codex: [[codex:react/components]] [[codex:react/props]] [[codex:react/jsx]]
