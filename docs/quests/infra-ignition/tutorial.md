# Tutorial

## Approach
This quest is designed to be solved by reading the problem statement and validating behavior against the tests.

## Implementation
- Identify the entrypoint file(s) referenced by the quest.
- Implement the smallest change that satisfies the failing test case first.
- Incrementally expand coverage until all tests pass.

## Testing
- Run the quest’s public tests locally.
- If there are multiple test cases, fix them one by one and re-run.

## Pitfalls
- Don’t overfit to a single test case; confirm behavior for all cases.
- Watch for edge cases called out in the prompt (empty inputs, nullables, ordering).
