# Tutorial — Service Boundaries

## What You’ll Learn
- How to isolate responsibilities into clear boundary surfaces
- How to shape inputs/outputs so tests can validate behavior cleanly
- How to avoid coupling by using small “contract” functions/modules

## Approach
Treat this quest like building a small service with a clean contract:
**inputs in → deterministic behavior → outputs out**, with side effects isolated (or eliminated).

## Implementation Plan
1. **Read the README spec**
   - Identify the required behavior and the “contract” (inputs/outputs).
2. **Locate the entrypoint**
   - Find the function/module the tests exercise (the first failing test usually reveals it).
3. **Implement the baseline path**
   - Start with the simplest valid case the tests expect.
4. **Enforce the boundary**
   - If logic is mixed (parsing + policy + formatting in one place), split responsibilities.
5. **Handle edge cases**
   - Follow what tests imply: empty inputs, invalid cases, ordering, defaults.

## Testing
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/python_systems.json --only-slug python-systems-service-boundaries
```

* Run once to see the first assertion failure.
* Fix *only what that failure requires*, then re-run.
* Repeat until green.

## Pitfalls

* Hardcoding values that only satisfy one test case
* Mixing concerns inside the boundary function (making it hard to reason about)
* Returning the right data but in the wrong shape/order

## If You’re Stuck

Use `hints.md` in order—Hint 3 should be enough to unblock you without reading a full solution.
