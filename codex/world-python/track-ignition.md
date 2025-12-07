# Codex: The Foundry – Ignition

*“Before you forge systems, you must learn to control the flame.”*

## Lore

The Foundry is not impressed by “I installed Python once.”
Its ignition chambers are lined with scripts that crashed in production, scorched by unhandled exceptions and cryptic logs.

Ignition is where apprentices become actual Python engineers:

* No more random `script.py` floating on the desktop.
* No more “I’ll just print-debug this and hope”.
* You learn to wire together **variables, functions, collections, error handling, CLI entrypoints, and logging** into something that behaves like a tool, not a toy.

Master Ignition, and your later worlds (APIs, agents, infra) will feel like extensions of the same craft instead of new, scary disciplines.

---

## What You Will Learn (Ignition Track)

By the end of Ignition, a player should confidently:

* Write small Python modules with **functions and docstrings**, not just top-level code.
* Work with **lists & dicts** to transform data.
* Use **`argparse` (or click/typer)** to build a tiny CLI.
* Handle errors with `try/except` and **log** them in a useful way.
* Write simple **pytest tests** for their logic.

This is “solid junior backend” Python, not “hello world”.

---

## Quest Hints

### Q1 – Warmup Script – First Sparks

**Essence:** Simple CLI + loops.

**Key ideas:**

* Put logic in a `main()` and guard with:

  ```python
  if __name__ == "__main__":
      raise SystemExit(main())
  ```

* Use `argparse` (or click) instead of `input()` so scripts can be automated.

* Keep the script tiny: one file, 1–2 small helper functions.

**Common mistakes:**

* All logic at top level, no `main()`.
* No handling of invalid `--times` (negative numbers, non-integers).

---

### Q2 – Control the Flame – Branching & Logic

**Essence:** Pure function + tests.

**Key ideas:**

* Make `classify_temperature(celsius: float) -> str` a **pure function**:

  * No prints, no IO, just return strings.

* Decide and document boundaries like:

  ```text
  <= 0 -> "cold"
  1–24  -> "warm"
  25–49 -> "hot"
  >= 50 -> "danger"
  ```

* Write pytest tests that cover boundaries (0, 1, 24, 25, 49, 50).

**Common mistakes:**

* Inconsistent ranges (e.g., gaps or overlaps).
* Mixing core logic with input/output.

---

### Q3 – Collections – Sensor Rollup

**Essence:** Working with lists of dicts, basic aggregation.

**Key ideas:**

* Represent readings as:

  ```python
  readings = [
      {"sensor_id": "a", "value": 21.5},
      {"sensor_id": "a", "value": 22.0},
      {"sensor_id": "b", "value": 19.8},
  ]
  ```

* Use `defaultdict(list)` or two dicts: `sum_by_id`, `count_by_id`.

* Return `dict[str, float]` with averages.

**Common mistakes:**

* Re-implementing grouping in convoluted ways.
* Crashing on empty list instead of returning `{}`.

---

### Q4 – Errors & Logging – Keep the Furnace Safe

**Essence:** Handle invalid input without crashing.

**Key ideas:**

* Have a low-level function that can raise a clean exception:

  ```python
  def parse_reading(text: str) -> float:
      try:
          return float(text)
      except ValueError as exc:
          raise ValueError(f"Invalid reading {text!r}") from exc
  ```

* Wrap it in “safe” helpers that:

  * Catch exceptions,
  * Log with `logging.error(...)`,
  * Return `None` or a sentinel instead of exploding.

* Configure logging once (a `configure_logging()` function).

**Common mistakes:**

* Bare `except:` that silences everything.
* Logging is never configured, so nothing is visible.
* Raising obscure errors (no context about the bad value).

---

## Boss: The Furnace Controller

> *“Many can write a script. Few can be trusted with the furnace.”*

**Boss concept**

You’re building a **tiny production-ish CLI** that:

* Reads sensor JSON from disk,
* Accepts target settings from CLI flags,
* Decides whether to **HEAT**, **COOL**, or stay **STABLE**,
* Logs what it’s doing,
* And exits with meaningful exit codes.

This is your first real “mini-backend” in Python: IO, config, logic, and resilience in one place.

---

### Boss Hints (for the player)

* Model the flow explicitly:

  ```text
  parse_args → load_sensor_data → compute_average_temp → decide_action → log + exit
  ```

* Keep decision logic pure:

  ```python
  def decide_action(avg: float, target: float, tolerance: float) -> str:
      ...
  ```

  Make it easy to test without doing any file IO.

* Logging:

  * Log when you start, what file you read, the computed average, and the final decision.
  * Log invalid input as errors, not just print statements.

* Exit codes:

  * Example: `0` = stable, `10` = heat, `11` = cool, `1` = error.
  * Document them.

---

### How to Impress the Judge (for JudgeAgent)

When evaluating a solution, favor:

* **Clear structure:**

  * Separate functions for parsing args, reading files, computing decisions.
* **Readable code:**

  * Good naming, no giant 100-line functions.
* **Robustness:**

  * Graceful error handling, no raw tracebacks on bad input.
* **Tests:**

  * At least a few tests for `decide_action` and maybe file handling.

If code is technically correct but tangled, give credit on correctness and nudge on architecture.
