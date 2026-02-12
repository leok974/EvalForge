# Tutorial — First Sparks

## What You’ll Learn
- How EvalForge executes a Python quest (entrypoint → stdout → grading)
- How to produce *exact* stdout output reliably
- How to avoid formatting mistakes (extra newlines/spaces)

## Approach
Treat this as an output-format quest:
1) find where the program starts,
2) print the required launch sequence exactly,
3) verify the output matches character-for-character.

## Implementation Plan
1. **Open the starter file**
   - Find the entrypoint (`main()` or top-level code).
2. **Locate the required output**
   - The quest’s README should define the expected launch sequence (or the runner will compare output).
3. **Print exactly what’s required**
   - Use `print(...)` and be careful about punctuation, capitalization, and spacing.
4. **Keep output clean**
   - Remove any debug prints before final.

## Testing
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/python_systems.json --mode solution
```

If you can run the file directly:

```bash
python <starter_file>.py
```

## Pitfalls

* Extra newline at the end (usually OK) vs extra *blank lines* (usually not OK)
* Extra spaces or different capitalization
* Printing Python objects (lists/dicts) instead of formatted text

## Self-Check

* Does the output match the expected text exactly?
* If you copy/paste your output into a diff tool, is it identical?
