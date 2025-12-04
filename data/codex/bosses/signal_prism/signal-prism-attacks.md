---
slug: boss-signal-prism-attacks
boss_id: signal_prism
tier: 2
world_id: world-prism
tags:
  - boss
  - signal_prism
  - attacks
  - mechanics
  - javascript
title: "The Signal Prism – Attack Patterns & Failure Modes"
---

> ZERO: "Signals are never 'clean'. Make your reducer ready for how users actually behave."

Once you've died a few times, ELARA releases structured intel on how the Prism breaks your code.

---

## 1. Out-of-Order Streams – "Refraction Lag"

**What it does:**

Occasionally delivers events **slightly out of order**:

- A `close` or `ack` event may arrive before a late `update`.
- A late `open` event might follow an earlier `close` with a higher `ts`.

**What it’s testing:**

- Do you always treat "last event by `ts` wins" per signal?
- Do you check `ts` when updating, or just trust array iteration order?

**Typical failures:**

- Applying events in the given order without comparing timestamps.
- Letting older events overwrite newer ones.
- Ending up with a closed signal that has a stale message or severity.

---

## 2. Duplicate Burst – "Echo Storm"

**What it does:**

Injects **duplicate events**:

- Same `id`, `kind`, and `ts`, sometimes repeated multiple times.
- Especially around `open` or `close`.

**What it’s testing:**

- Is your reducer **idempotent** for duplicates?
- Do you accidentally create multiple SignalState entries per `id`?

**Typical failures:**

- Pushing a new `SignalState` for each `open` instead of updating in place.
- Ending with duplicates in the final array.
- Using index-based logic instead of id-based maps.

---

## 3. Partial Payloads – "Light Fragments"

**What it does:**

Sends `update` events with **only part of the payload**:

- `severity` but no `message`.
- `message` but no `severity`.
- Empty payloads that still carry meaningful `kind` and `ts`.

**What it’s testing:**

- Do you treat payload fields as **patches** instead of full replacements?
- Do you accidentally wipe valid fields when a partial update arrives?

**Typical failures:**

- Overwriting the whole `payload` instead of merging.
- Resetting severity to a default when no severity is provided.
- Dropping the existing message on a severity-only update.

---

## 4. Channel Mismatch – "Cross-Beam"

**What it does:**

Delivers events on **different channels** for the same `id`:

- A signal might start on `"system"` but get updated on `"network"` by mistake.

**What it’s testing:**

- Do you treat `channel` as immutable per `id`?
- Or do you let later events silently rewrite it?

**Typical failures:**

- Allowing channel to flip mid-stream and ending with inconsistent panels.
- Ignoring channels entirely in the final state.

---

## 5. Quiet Flood – "Dimmed Noise"

**What it does:**

Sends **long sequences of benign events**:

- Many low-severity events, or updates that don't change much.

**What it’s testing:**

- Does your reducer remain reasonably efficient on larger inputs?
- Are you doing unnecessary nested scans or repeated copies?

**Typical failures:**

- O(n²) operations over the events + states on each iteration.
- Over-allocating arrays or rebuilding large structures more than needed.
- Creating a new Map or object graph inside every loop for no reason.

---

### Summary

If your reducer:

- Uses a **Map keyed by id**,
- Compares `ts` before applying an update,
- Merges partial payloads instead of replacing blindly,
- Returns a clean, deduplicated array at the end,

…then most of the Prism's attacks pass straight through.

Otherwise, the panel flickers — and so does your Integrity.
