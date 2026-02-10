# Briefing — React Lists: User Directory

## Objective
Implement `UserList` to render a list of users as `<li>` elements with proper keys.

## Context
Rendering lists is about two things:
1) mapping data → elements, and  
2) giving React stable **keys** so it can reconcile updates correctly.

## Where You’ll Work
- Edit: `data/quests/react-lists/workspace/task.mjs`
- Tests: `data/quests/react-lists/grading/public/react-lists.public.test.mjs`
- Fixture: `data/quests/react-lists/workspace/fixtures/users.json`

## Requirements
1. Accept `users` (array of `{ id, name }`).
2. Render a `ul` with `data-testid="user-list"`.
3. Render an `li` for each user.
4. Each `li` MUST have `key` set to the user’s `id`.
5. Each `li`’s content is the user’s `name`.

## Constraints
- ✅ No JSX — use `React.createElement`
- ✅ Keys must be stable and unique (use `user.id`)

## Success Criteria
- [ ] `ul[data-testid="user-list"]` exists
- [ ] One `li` per user
- [ ] `li` children match user names in order
- [ ] Each `li` has `key=user.id` (likely enforced via hidden tests / runtime warnings)
- [ ] Public tests pass

## How To Verify
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Spec and Codex References

* Spec: `README.md` (this quest)
* Codex: [[codex:react/lists-and-keys]] [[codex:react/props]] [[codex:react/components]]
