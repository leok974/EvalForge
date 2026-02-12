# Briefing — First Sparks

## Objective
Initialize the Python runtime by printing the quest’s **launch sequence** exactly in the expected format.

## Context
This quest is your “power-on” moment: you’re practicing the absolute basics of Python execution and stdout formatting. The main thing being evaluated here is **exact output**.

## Where You’ll Work
- Edit: the provided starter file in `docs/quests/first-sparks`’s workspace (check the quest folder for the exact filename).
- Runner/Checks: this quest likely validates **stdout + exit code** via the EvalForge runner.

## Requirements
1. Implement the solution in the provided starter file.
2. Use standard library features where appropriate.
3. Verify output matches the expected format.

## Constraints
- ✅ Don’t add extra text, debug prints, or whitespace beyond what the expected output requires.
- ✅ Keep it simple and deterministic.

## Success Criteria
- [ ] Script runs without errors (exit code 0)
- [ ] Output matches the expected launch sequence format exactly
- [ ] No extra output lines or spacing differences

## How To Verify
Run the Python questpack (or world runner) and confirm it’s green:

```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/python_systems.json --mode solution
```

If there’s no explicit test file, also run the starter directly (path depends on your quest workspace):

```bash
python <starter_file>.py
```

## Spec and Codex References

* Spec: `README.md` (this quest)
* Codex: Use the Codex panel for “printing / stdout / entrypoints” concepts as needed.
