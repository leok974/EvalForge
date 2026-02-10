# Briefing — React Effects: Mount/Unmount

## Objective
Implement `LifecycleLogger` so it calls `onMount` when mounted and `onUnmount` when unmounted (via effect cleanup).

## Context
Effects are for work that happens “around” rendering: lifecycle behavior, subscriptions, timers, etc. This quest drills the **mount** effect and **cleanup**.

## Where You’ll Work
- Edit: `data/quests/react-effects-mount/workspace/task.mjs`
- Tests: `data/quests/react-effects-mount/grading/public/react-effects-mount.public.test.mjs`

## Requirements
1. Accept props `onMount` and `onUnmount` (functions).
2. Use `useEffect` to call `onMount` when the component mounts.
3. Return a cleanup function that calls `onUnmount`.
4. Render `null` or any element.

## Constraints
- ✅ No JSX — use `React.createElement` if you render anything
- ✅ Use an effect; mount call should happen once per mount

## Success Criteria
- [ ] `onMount` called exactly once after mounting
- [ ] `onUnmount` not called immediately
- [ ] Cleanup calls `onUnmount` when unmounted (likely hidden test)
- [ ] Public tests pass

## How To Verify
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Spec and Codex References

* Spec: `README.md` (this quest)
* Codex: [[codex:react/effects]] [[codex:react/events]] [[codex:react/components]]
