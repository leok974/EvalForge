# Briefing — Service Boundaries

## Objective
Implement the required behavior for **python-systems-service-boundaries** so all public tests pass.

## Context
This quest is about **service boundaries**: keeping responsibilities separated, avoiding leaky abstractions, and making it easy to test behavior without coupling everything together.

## Where You’ll Work
- Primary file(s): (see **README.md** for exact paths)
- Tests: (see **README.md** / questpack)

## Requirements
- ✅ Complete the assignment as described in **README.md**
- ✅ Preserve intended boundaries (don’t “just make the test pass” by hardcoding)
- ✅ Keep changes minimal and readable

## Constraints
- Follow the quest constraints described in the prompt and starter code.
- Prefer small, test-driven changes; avoid extra dependencies unless explicitly allowed.

## Success Criteria
- [ ] All public tests pass for this quest
- [ ] Implementation matches expected function signatures and output shapes
- [ ] No unnecessary complexity or hidden side effects

## How To Verify
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/python_systems.json --only-slug python-systems-service-boundaries
```

## Spec and Codex References

* README: `README.md` (this quest’s source-of-truth spec)
* Codex: [[codex:systems/service-boundary]] [[codex:testing/mock]] [[codex:interfaces/contracts]]
