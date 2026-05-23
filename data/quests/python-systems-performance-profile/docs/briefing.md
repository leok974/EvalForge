# Briefing: Performance & Profiling

## The Mission
The Reactor Core's query engine is stalling. As our datasets grow, the time spent searching for matching records is increasing exponentially. We suspect that our current "naive" membership checks are the bottleneck.

Your mission is to analyze the performance of two different search strategies:
1.  **Naive Comparisons**: A simple list-based search.
2.  **Set Operations**: Using hash-based sets for near O(1) membership checks.

You must implement a deterministic cost model for both strategies and a logic to choose the most efficient one based on the calculated costs.

## Objectives
- Implement `naive_comparisons`: Count every single comparison (item == query) performed in a nested loop.
- Implement `set_ops`: Count the "ops" for building the set (len(items)) plus the number of membership lookups (len(queries)).
- Implement `choose_strategy`: Select the cheaper cost. If they are equal, prefer the `"set"` strategy.
- Return a report containing the total "hits", the chosen strategy, and the cost breakdown.

## Constraints
- Do not use `time.time()` (we need deterministic results). Use the cost model described.
