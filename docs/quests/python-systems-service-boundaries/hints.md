# Hints — Service Boundaries

## Hint 1 (nudge)
The tests are checking a **contract**. Focus on shaping the output exactly as expected (types/keys/order), and keep side effects out of the core logic.

## Hint 2 (more specific)
Look for the first failing assertion and trace backwards:
- What input did the test pass in?
- What output shape is expected?
The entrypoint is usually the function named in the failure message or the module imported by the test.

## Hint 3 (close)
If the logic feels tangled, split it into:
- a “pure” function that does transformation/validation
- a wrapper that handles any I/O (if any exists)
Then test expectations should align naturally.

## Hint 4 (optional spoiler)
> Spoiler: The cleanest fix is usually to make the boundary function return a single normalized structure and keep parsing/formatting outside.
