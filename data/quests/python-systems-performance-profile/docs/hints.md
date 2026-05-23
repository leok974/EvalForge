# Hints: Performance & Profiling

## Hint 1 — Concept
For `naive_comparisons`, make sure to increment your counter *inside* the inner loop, *before* the equality check. Every comparison counts!

## Hint 2 — Guided
Remember that `count_hits` should be a clean implementation using a `set` for efficiency, but not necessarily tied to your cost model counters.

## Hint 3 — The Solution
Tie-breaking is important. If the costs for `naive` and `set` are exactly equal, the system expects you to return `"set"` as the chosen strategy.
