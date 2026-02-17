# Tutorial — Hello Variable

## What You’ll Learn
- Variable naming and assignment
- String literals and exact matching
- Minimal “main program” patterns

## Approach
Do the smallest correct thing:
1) define `message`,
2) use it in output,
3) keep formatting exact.

## Key Terms
- **[variable](codex:glossary/python/variable)**
- **[print](codex:glossary/python/print)**

## Implementation Plan
1. In `main()`, create the variable:
   - `message = "System Online"`
2. Output it (if the quest expects printing):
   - `print(message)`
3. Ensure `main()` runs when the script executes:
   - `if __name__ == "__main__": main()`

## Testing
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/python_systems.json --mode solution
```

## Pitfalls

* Naming the variable `msg` or `Message` instead of `message`
* Using single vs double quotes is fine in Python, but the *string content* must match
* Forgetting to call `main()` so nothing runs

## Self-Check

* Is there a variable literally named `message`?
* Does the program produce visible output when run?
