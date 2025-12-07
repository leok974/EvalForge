# Reference Review – Data Crucible (Gold Solution)

**Verdict:** ✅ *Strong pass*

### What this solution gets right

1. **Config-first design**

   * Uses a `CrucibleConfig` dataclass with a clear `from_dict` validator.
   * Fails fast on bad config (missing `group_by` / `value_field`).

2. **Separation of concerns**

   * IO:

     * `load_config`, `load_rows`, `write_output`.
   * Core logic:

     * `aggregate(rows, group_by, value_field)` is **pure** and fully testable.
   * Orchestration:

     * `main()` wires everything together and handles logging.

3. **Robust error handling**

   * Raises meaningful `ValueError`s when:

     * Group-by columns are missing.
     * Value field is missing or non-numeric.
     * CSV/config file missing or malformed.
   * CLI exits with code `1` on failure and logs errors instead of crashing.

4. **Output shape & stability**

   * Output JSON entries include:

     * All `group_by` fields.
     * Metrics: `sum`, `count`, `avg`.
   * Sorting result by group keys makes output deterministic (good for tests and diffs).

5. **Testing**

   * Tests cover:

     * Config parsing.
     * Basic aggregation (sum/count/avg) with multiple groups.
     * Failure case (missing group column).

### How to compare student submissions

Use this as a baseline:

* **Strong solution (pass with distinction):**

  * Has a clearly separated pure `aggregate` function.
  * Respectfully validates config and data, with clear error messages/logging.
  * Produces grouped JSON with at least `sum` and `count` (avg optional).
  * Has tests for both success and failure paths.

* **Sufficient solution (pass):**

  * Correctly groups and sums according to config.
  * Handles missing files / totally broken config gracefully.
  * Some structure (a couple of helper functions).
  * Minimal tests for happy path, maybe no explicit failure tests.

* **Borderline / needs work:**

  * Hard-codes grouping logic instead of using config.
  * All logic in `main()`; still technically correct but difficult to test.
  * Crashes on obvious errors or returns confusing errors.

* **Fail:**

  * Ignores config; just prints ad-hoc stats.
  * Fails for basic input or cannot run end-to-end.
  * No attempt at error handling or tests.

### Suggested feedback snippets for JudgeAgent

You can reuse lines like:

* “Great use of a pure `aggregate()` function; this makes your transformation easy to test.”
* “Config is only partially used; try to make `group_by` and `value_field` truly drive the behavior instead of hard-coding them.”
* “Consider raising a clear `ValueError` when required columns are missing, and logging that instead of letting a `KeyError` leak out.”
* “All logic is bundled into `main()`. Splitting into `load_rows` / `aggregate` / `write_output` will make this more maintainable and testable.”
