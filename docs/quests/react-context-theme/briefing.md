# Briefing — React Context: Theme

## Objective
Implement a theme context flow: a provider that supplies a theme string, and a button that consumes it.

## Context
Context is for values that many components need without passing props through every layer. This quest drills:
- create context
- provider value
- consumer via `useContext`

## Where You’ll Work
- Edit: `data/quests/react-context-theme/workspace/task.mjs`
- Tests: `data/quests/react-context-theme/grading/public/react-context-theme.public.test.mjs`

## Requirements
1. Create a Context (not exported).
2. Export `ThemeProvider`:
   - Props: `children`, `theme` (string)
   - Render the Context Provider with `value={theme}` around children
3. Export `ThemedButton`:
   - Consume context theme
   - Render `button[data-testid="btn"]`
   - Button text is the theme value

## Constraints
- ✅ Context object itself is not exported
- ✅ No JSX — use `React.createElement`

## Success Criteria
- [ ] Provider passes `theme` via context
- [ ] ThemedButton reads theme via `useContext`
- [ ] Button text equals the theme string (e.g., `"dark"`)
- [ ] Public tests pass

## How To Verify
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Spec and Codex References

* Spec: `README.md` (this quest)
* Codex: [[codex:react/context]] [[codex:react/components]] [[codex:react/props]]
