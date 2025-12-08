---
title: "Boss: Foundry Systems Architect"
id: "boss-foundry-systems-architect"
type: "boss-codex"
world: "world-python"
track: "foundry-senior-systems"
difficulty: "hard"
---

# 🏗️ Boss: Foundry Systems Architect

> "Legacy code is just a monument to past decisions. Your job is to enable the future."

## 📜 The Mission

You have inherited a critical legacy system: `Monolithos`, a sprawling Python application that powers the Foundry's core logistics. It is brittle, slow, and impossible to deploy without downtime.

Your mission is to design and implement a **Modernization Runbook** and a **Prototype Refactor** for `Monolithos`. You must carve out a clean service boundary, introduce resilience patterns, and establish observability without breaking the existing flow.

## 🧱 The Codebase Context

The existing system is a single Django/Flask-like application (simulation) with:
-   A god-object `OrderManager` class (3000+ lines).
-   Tightly coupled database calls scattered in views.
-   Synchronous calls to external third-party APIs that frequently timeout.
-   Zero metrics or structured logs.

## 🎯 Objectives

1.  **Define Service Boundaries**: Identify the "Logistics" domain and extract it into a clean module with a strict interface (Facade/Port-Adapter).
2.  **Resilience Layer**: Implement a `CircuitBreaker` and `Retry` mechanism for the flaky external "Supplier Protocol" API.
3.  **Observability Integration**: Instrument the critical path with `structured_logging` (correlation IDs) and basic SLI metrics (latency histogram).
4.  **Async Migration**: Convert the blocking email notification system to an asynchronous job queue (simulated with `asyncio` loop).

## 🧩 The Boss Fight (Technical Challenges)

### Phase 1: The Tangle (Refactoring)
*   **Attack**: "Dependency Sprawl" - The boss introduces circular imports and hidden side effects.
*   **Defense**: Dependency Injection. You must decouple the `NotificationService` and `DatabaseRepo` from the core logic.

### Phase 2: The Flake (Resilience)
*   **Boss Move**: "Latency Spike" - The external `SimulatedSupplierAPI` will fail 50% of requests and hang for 5 seconds on others.
*   **Counter**: Implement a circuit breaker that fails fast and a fallback mechanism (caching or default response).

### Phase 3: The Black Box (Observability)
*   **Boss Move**: "Silent Failure" - Requests drop without logs.
*   **Counter**: Ensure every request has a `trace_id` propagated through the layers and logs the final status.

### Phase 4: The Bottleneck (Concurrency)
*   **Boss Move**: "The Thundering Herd" - 1000 orders arrive at once, blocking the main thread.
*   **Counter**: Offload the heavy "Invoice PDF Generation" task to an async worker queue.

## 🛡️ Constraints & Rules

1.  **No Rewrite from Scratch**: You must refactor the existing `Monolithos` class, not delete it.
2.  **Type Safety**: All new boundaries must use strict Python type hints (`typing.Protocol`, `pydantic`).
3.  **Testing**: You must provide a `pytest` suite that verifies the circuit breaker behavior and happy path.

## 🔮 Hint

> "The Strangulate Vine pattern is your friend. Do not slice the monolith all at once; wrap it, interface it, then replace the guts."
