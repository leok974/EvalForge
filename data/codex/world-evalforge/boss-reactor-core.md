---
id: boss-reactor-core
title: "Strategy Guide: The Reactor Core"
world: world-evalforge
type: strategy_guide
summary: Tactics for stabilizing the core logic.
---

# Boss Mechanics
The Reactor Core tests your ability to handle **Async Concurrency** and **Error Propagation**.

# Common Pitfalls
- ❌ **Blocking the Loop:** Using `time.sleep()` instead of `asyncio.sleep()` will cause immediate containment failure.
- ❌ **Swallowing Exceptions:** The Core requires precise error reporting. Do not use bare `try/except` blocks.

# Winning Strategy
Use `asyncio.gather` to manage the cooling rods in parallel. Ensure you return a `dict` with the key `status: "STABLE"`.
