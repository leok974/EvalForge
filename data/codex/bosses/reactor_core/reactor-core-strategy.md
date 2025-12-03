---
slug: boss-reactor-core-strategy
boss_id: reactor_core
tier: 3
world_id: world-python
tags:
  - boss
  - reactor_core
  - strategy
  - python
  - testing
  - design
title: "The Reactor Core – Strategy & Survival Guide"
---

> ELARA: "Architect, you have enough data. Time to design like it matters."

You unlocked this file by **defeating the Reactor Core**.  
This is a **full strategy guide**. It will absolutely make the fight easier for future runs.

Use it to internalize patterns, not to skip thinking.

---

## 1. Start With the Contract, Not the Code

Before touching the starting code:

1. Re-read the **problem spec** as if it were a real ticket:
   - Inputs and their shapes.
   - Outputs and guarantees.
   - Error conditions.
2. Write down (in comments) the **contract** of your main function:
   - Parameters and allowed values.
   - Return type and invariants.
   - Edge cases you must handle.

Treat the spec like a miniature **API design doc**.

---

## 2. Build a Mental Test Plan First

The boss has hidden tests, but you can approximate them:

- **Happy path cases** – the examples in the prompt.
- **Boundary cases** – smallest and largest allowed values.
- **Null / empty cases** – `""`, `[]`, `{}`, `None`.
- **Mis-shaped input** – missing keys, extra keys.
- **Large batch** – a realistic number of repeated calls or items.

Write some **quick local tests** or assertions in the starting code:

```python
def _self_test():
    # happy path
    assert fn(valid_input_1) == expected_output_1
    # boundary
    assert fn(boundary_input) == expected_boundary_output
    # empty
    assert fn(empty_input) == expected_empty_output
```

You don’t need a full framework to think like a tester.

---

## 3. Design for Clarity First, Then Efficiency

The Reactor Core punishes horrible complexity, not normal Python.

You almost always want:

* **Small helper functions** with clear names.
* A **single responsibility** for each function.
* A simple, consistent **data shape** in and out.

Example pattern:

```python
def process_batch(items: list[dict]) -> list[dict]:
    return [process_item(item) for item in items if is_valid(item)]
```

Where:

* `is_valid` has **all the validation logic**.
* `process_item` is pure: input → output, no side effects.
* You never mutate the input in-place unless the spec demands it.

If your solution is easy to explain, it usually stands up better to the boss rubric.

---

## 4. Handle Edge Cases Explicitly

Don’t “hope” that empty inputs just work.

Be deliberate:

```python
def process_batch(items: list[dict]) -> list[dict]:
    if not items:
        return []

    # rest of logic…
```

And for individual fields:

```python
value = row.get("value")
if value is None:
    # decide: skip? default? error?
```

If the spec doesn’t say how to handle a case, make a **reasonable, consistent choice** and apply it everywhere.

---

## 5. Return Helpful, Stable Shapes

Avoid returning:

* `None` sometimes and a list/dict other times.
* Mixed types in a list unless explicitly requested.

Prefer:

* **Always** return a list (possibly empty).
* **Always** return a dict with a stable set of keys.

If the spec allows error reporting, standardize it:

```python
{
  "ok": False,
  "error": "Missing required field 'x'",
}
```

This is exactly the kind of thing JudgeAgent’s rubric can reward.

---

## 6. Use Logging Intentionally (If Available)

If the boss environment supports logging, treat logs as **your black box recorder**:

* Log at **debug/info** for major branches:

  * “Skipping row with missing id”
  * “Processed 250 items”
* Log at **warning/error** for actual failures:

  * “Invalid value for field 'status': …”

Don’t spam. Aim for “if this fails, would this log tell me why?”

Even when logs are not visible in the UI, the rubric can still reward **structured error handling** and clear failure modes.

---

## 7. Surviving Multiple Attempts

You will probably not one-shot the Reactor Core. That’s normal.

Use each failure run as **training data**:

1. After a failure, note what changed:

   * Integrity loss magnitude.
   * Any hints or comments from ZERO / KAI.
2. Map that to a category:

   * “Probably edge cases”
   * “Probably performance”
   * “Probably inconsistent return types”

Iterate with intention:

* If you suspect **edge cases**, audit validation and empty inputs.
* If you suspect **performance**, look for nested loops and duplicate work.
* If you suspect **contract violations**, triple-check types and shapes.

---

## 8. Pattern Library: When in Doubt, Use These

**Safe patterns for Reactor Core–style problems:**

* Pure functions with no global state.
* Small local helpers that each do one thing:

  * `parse_input`
  * `validate_record`
  * `transform_record`
  * `summarize_results`
* Immutable thinking: derive **new** data structures instead of mutating complex ones in-place.
* Explicit, consistent error handling.

If you reach for these patterns automatically, future bosses in other worlds (JS, SQL, Infra, Agents) will also hurt less.

---

> ZERO: "Unit. The Reactor is not here to kill you. It is here to measure if you are worth deploying."
> ELARA: "And now, Architect, you have the intel to make that answer ‘yes’ on the first try."
