# Codex: Reactor Ops Conductor

The Core Controller keeps the Reactor stable.  
The Ops Conductor keeps **humans** stable.

This boss is about **operability**:

- How the service starts
- How it logs
- How it shuts down
- How it reacts to different environments

---

## Mission

Use your existing pieces:

- `StableCoreController`
- `ReactorConfig`
- Logging (SLF4J + backend)
- Build tool (Maven/Gradle)

Design two types:

1. `ReactorOpsConductor` – encapsulates the run loop and lifecycle.
2. `ReactorOpsMain` – a small `public static void main` that wires everything and delegates.

The service should:

- Load configuration (defaults + env overrides).
- Construct `ReactorRegistry`, `ReactorController`, `StableCoreController`.
- Run a loop that:
  - Reads or synthesizes `SensorReading`s,
  - Calls `stable.tickCore(...)`,
  - Sleeps (e.g., fixed period),
  - Stops when signaled.

- Handle **graceful shutdown**:
  - Respond to SIGINT/SIGTERM or a shutdown flag.
  - Log startup and shutdown clearly.
  - Exit with a non-zero status on severe startup failure.

---

## Design Hints

- **Separation of concerns**

  - `ReactorOpsConductor` should not parse CLI args or system properties directly.
  - `ReactorOpsMain` can parse args, choose environment, and create the config object.

- **Loop design**

  - Prefer a simple `while (running)` loop with clear exit conditions.
  - Avoid busy loops: sleep between ticks.
  - Expose a `stop()` or `close()` method for tests to halt the loop quickly.

- **Signals**

  - Use logs to communicate state transitions:
    - starting, started, stopping, stopped
    - environment in use (dev, staging, prod)
    - config highlights (e.g., thresholds)

---

## What the Judge Cares About

- **Operability**
  - Would an on-call engineer understand what the service is doing from logs alone?
  - Is there a single place to start/stop the loop?

- **Config integration**
  - No hidden magic numbers where `ReactorConfig` should be used.
  - Environment overrides flowing through cleanly.

- **Testability**
  - Can you run a shortened loop in tests?
  - Can you simulate shutdown without sending real signals?

If your Reactor Ops Conductor looks like a small, production-grade worker service, you’ll have satisfied the boss.
