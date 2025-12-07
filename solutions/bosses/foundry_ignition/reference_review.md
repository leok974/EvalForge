# Reference Review – Furnace Controller (Gold Solution)

**Overall verdict:** ✅ *Strong pass*

The solution demonstrates:

1. **Clear structure**

   * Logic is split into small, focused functions:

     * `parse_args`, `configure_logging`, `load_sensor_data`, `compute_average`, `decide_action`, `main`.
   * `decide_action` and `compute_average` are pure functions, making them easy to test.

2. **Correctness & robustness**

   * Handles:

     * Missing file (`FileNotFoundError`),
     * Invalid JSON (`JSONDecodeError` → `ValueError`),
     * Empty or malformed `readings`.
   * Uses meaningful error messages with context about which file/value failed.
   * Exit codes have a clear mapping:

     * `0` = stable, `10` = heat, `11` = cool, `1` = error.

3. **Logging**

   * Logs:

     * Startup info (file, target/tolerance),
     * Average temperature,
     * Final decision,
     * Errors when reading/processing data.
   * Uses the standard logging module instead of `print`.

4. **Testing**

   * Tests cover:

     * Stable vs HEAT vs COOL logic.
     * Average computation, including an error case.
   * Logic is testable without running the CLI.

**Minor improvement suggestions** (for JudgeAgent to use as “nice to have” feedback):

* Add at least one **docstring** explaining the JSON input format more explicitly (e.g., sample payload).
* Consider extracting exit code mapping into a small helper or constant dict for readability.
* Consider adding a very small integration test that runs `main([...])` with a temporary JSON file.

**How to use this reference when grading other submissions:**

* If a learner’s solution:

  * Has similar decomposition into functions, uses logging, and handles bad inputs → treat as **strong**.
  * Puts everything into `main` but still meets requirements and doesn’t crash → **passing**, but suggest refactoring into smaller functions.
  * Hard-codes a single reading or ignores CLI arguments → **partial** at best; call out correctness gaps.
  * Lacks logging and crashes on bad input → **fail** on robustness, even if happy path works.
