# Codex: Stable Core Controller

> *“Power is easy. Stability is hard.”*

The Reactor can’t be trusted to a single class or clever trick. A stable core comes from **clear orchestration**:

- **Inputs:** sensor readings.
- **Decisions:** control logic.
- **State:** registry and core implementations.
- **Outcomes:** actions applied + alarms raised.

The Stable Core Controller is the conductor of this small Java orchestra.

---

## Mission

Use your Core Circuit pieces:

- `SensorReading`
- `InvalidReadingException`
- `ControlAction` (enum)
- `ReactorController` (logic that maps readings → ControlAction)
- `ReactorRegistry` (maps `coreId` → `ReactorCore`)

Design a module with two main types:

- `CoreTickResult` – a value object summarizing one tick.
- `StableCoreController` – the orchestrator.

Minimum API:

```java
public final class CoreTickResult {
    private final String coreId;
    private final boolean coreFound;
    private final boolean invalidReading;
    private final ControlAction action;
    private final List<String> alarms;

    // getters, constructor, builder/factory as you like
}

public final class StableCoreController {

    public StableCoreController(
        ReactorRegistry registry,
        ReactorController controller,
        AlarmSink alarmSink // interface you define
    ) { ... }

    public CoreTickResult tickCore(String coreId, SensorReading reading) {
        // 1) lookup core
        // 2) call controller.adjustCore(reading)
        // 3) apply action or handle InvalidReadingException
        // 4) raise alarms via AlarmSink
        // 5) return CoreTickResult
    }
}
```

You can extend this, but keep the surface **small and coherent**.

---

## What the Controller Should Do

1. **Lookup**

* Ask `ReactorRegistry` for the core by `coreId`.
* If missing:

  * Raise an alarm like `"CORE_NOT_FOUND:<coreId>"`.
  * Return a `CoreTickResult` with `coreFound=false` and a safe default action (e.g., `ControlAction.SHUTDOWN`).

2. **Decision**

* Call `ReactorController.adjustCore(reading)` to get a `ControlAction`.
* Handle `InvalidReadingException`:

  * Raise an alarm like `"INVALID_READING:<details>"`.
  * Return a `CoreTickResult` with `invalidReading=true` and `ControlAction.SHUTDOWN`.

3. **Application**

* When both core and reading are valid:

  * Apply the action to the `ReactorCore` (e.g., `core.applyControl(action)`).
  * Optionally raise alarms for critical actions (e.g., shutdown/overheat).

4. **Summary**

* Build a `CoreTickResult` that tells the story:

  * Which core?
  * Was it found?
  * Was the reading valid?
  * Which action?
  * Which alarms were raised?

---

## Design Principles

The Guardian cares about:

* **Clear layering**
  `StableCoreController` should not contain raw sensor parsing, low-level I/O, or global state. It orchestrates existing components.

* **Enums & value objects**
  Use `ControlAction` and a small `CoreTickResult` data type—no random strings.

* **Explicit error paths**
  Invalid cores and readings are modeled explicitly (booleans in `CoreTickResult` + alarms), not hidden in logs only.

* **Testability**
  You should be able to unit-test `StableCoreController` with fake `ReactorRegistry`, `ReactorController`, and `AlarmSink`.

If your solution is something you’d confidently ship as a small module in a production Java service, you’ve passed the trial.
