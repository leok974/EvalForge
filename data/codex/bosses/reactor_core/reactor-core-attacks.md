---
slug: boss-reactor-core-attacks
boss_id: reactor_core
tier: 2
world_id: world-python
tags:
  - boss
  - reactor_core
  - attacks
  - mechanics
  - python
title: "The Reactor Core – Attack Patterns & Failure Modes"
---

> ZERO: "Unit, the Core is predictable. Your failures are not. Fix that."

Once you’ve encountered the Reactor Core a few times (and probably died), ELARA begins releasing actual attack data.

Below are the **main mechanics** the boss uses to break your code.

---

## 1. Input Surge – “Stress Test”

**What it does:**  
Sends a large batch of inputs through your main entrypoint.

**What it’s testing:**

- Can your implementation handle **many calls** without degrading badly?
- Do you do anything **needlessly expensive** inside the hot path?
- Are you creating heavy objects on each request that you don’t need to?

**Typical failures:**

- O(n²) or worse logic on each call.
- Re-parsing static config or compiling regexes on every request.
- Using global mutable state that trips on concurrency in tests.

> Hint: If your function can’t handle “a lot of reasonable calls in a row,” the Core will find it.

---

## 2. Edge Storm – “Sad Path Barrage”

**What it does:**  
Pushes a curated set of **edge and broken inputs** at your code:

- Empty strings / lists / dicts
- Missing fields / unexpected keys
- Wrong types where the spec allows for it (e.g. `""` vs `None`)

**What it’s testing:**

- Do you read the **spec carefully**, including constraints?
- Do you **validate** before assuming structure?
- Do you fail **cleanly** (controlled exceptions, helpful messages) instead of exploding?

**Typical failures:**

- Indexing into empty lists without checks.
- Assumptions like `"key" in data` always being true.
- Returning inconsistent types on error.

---

## 3. Drift Pulse – “Spec Drift”

**What it does:**  
Uses tests that are **valid per the written spec** but *slightly different* from examples:

- Additional optional fields present.
- Different ordering of items.
- Larger but still valid values within constraints.

**What it’s testing:**

- Did you **hard-code** to the examples, or implement the **spec**?
- Are you depending on **incidental behaviors** (like key order) you don’t control?

**Typical failures:**

- Code that quietly ignores certain valid cases.
- Sorting or assumptions that aren’t required by the spec.
- Using fragile string parsing where structured data is available.

---

## 4. Blackout – “Error Handling”

**What it does:**  
Triggers a **controlled failure** path:

- Forces internal errors (e.g. bad configuration, missing dependency).
- Checks what your code **returns or logs** when things go wrong.

**What it’s testing:**

- Do you let raw stack traces leak or return nonsense?
- Do you provide **clear error messages** or structured error objects?
- Are you using exceptions **intentionally** instead of everywhere?

**Typical failures:**

- Returning `None` where the contract says “always a dict / list”.
- Swallowing exceptions silently.
- Raising a vague `Exception("Something went wrong")` everywhere.

---

## 5. Integrity Drain – “Partial Success”

**What it does:**  
Runs compound scenarios where **only some** inputs are bad.

**What it’s testing:**

- Can you **partially process** data without corrupting the rest?
- Do you treat failures as all-or-nothing when you don’t need to?
- Do you surface **which parts failed**?

**Typical failures:**

- Aborting the whole batch on a single bad item.
- Mutating input data in-place and leaving it in an inconsistent state.
- Returning a result that looks “ok” but hides corrupted entries.

---

## Summary: How the Core Kills You

The Reactor Core doesn’t rely on randomness. It relies on:

1. **Volume** – to punish slow or wasteful code.  
2. **Edge cases** – to punish assumptions.  
3. **Spec drift** – to punish cargo-culting examples.  
4. **Error handling checks** – to punish opaque failure modes.  
5. **Compound scenarios** – to punish all-or-nothing thinking.

If you don’t systematically close these gaps, Integrity will keep dropping, and so will you.
