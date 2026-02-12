# Briefing — Performance & Profiling

## Objective
Compute a deterministic profile report for membership queries and choose the cheaper strategy.

## What This Trains
- Finding the hot path (membership checks)
- Profiling without timing (operation counts)
- Choosing an optimization based on measured cost

## Success Criteria
- Output JSON deep-equals expected.
- Strategy selection follows tie-break rules.
- One canonical JSON line to stdout, no extra prints.
