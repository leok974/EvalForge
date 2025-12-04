---
slug: boss-signal-prism-strategy
boss_id: signal_prism
tier: 3
world_id: world-prism
tags:
  - boss
  - signal_prism
  - strategy
  - javascript
  - typescript
  - reducers
title: "The Signal Prism – Strategy & Survival Guide"
---

> ELARA: "Light is just data. Your job is to refract it into something a human can read."

You unlocked this file by **defeating the Signal Prism**.

This is a direct strategy guide. Expect spoilers.

---

## 1. Think in Maps, Not Arrays

The core pattern:

```ts
function computeSignalPanel(events: SignalEvent[]): SignalState[] {
  const byId = new Map<string, SignalState>();

  for (const event of events) {
    const prev = byId.get(event.id);
    const next = applyEvent(prev, event);
    if (next) {
      byId.set(event.id, next);
    } else {
      byId.delete(event.id);
    }
  }

  return Array.from(byId.values());
}
```

Where:

* `prev` is the current state for this `id` (or `undefined`).
* `applyEvent` handles `open`, `update`, `close`, `ack` with timestamp checks.
* Setting `next` to `null` or `undefined` can represent "remove this signal".

This naturally avoids:

* Duplicates in the final array.
* Index-based weirdness.

---

## 2. Centralize Timestamp Logic

All ordering rules belong in **one place**:

```ts
function shouldApply(prev: SignalState | undefined, ev: SignalEvent): boolean {
  if (!prev) return true;
  return ev.ts >= prev.lastEventAt;
}
```

Then:

```ts
function applyEvent(prev: SignalState | undefined, ev: SignalEvent): SignalState | null {
  if (!shouldApply(prev, ev)) {
    return prev ?? null;
  }

  switch (ev.kind) {
    case "open":
      return {
        id: ev.id,
        channel: prev?.channel ?? ev.channel,
        severity: ev.payload?.severity ?? prev?.severity ?? "info",
        message: ev.payload?.message ?? prev?.message ?? "",
        open: true,
        acknowledged: false,
        lastEventAt: ev.ts,
      };
    case "update":
      if (!prev) return null; // or decide to implicitly open
      return {
        ...prev,
        severity: ev.payload?.severity ?? prev.severity,
        message: ev.payload?.message ?? prev.message,
        lastEventAt: ev.ts,
      };
    case "ack":
      if (!prev) return null;
      return {
        ...prev,
        acknowledged: true,
        lastEventAt: ev.ts,
      };
    case "close":
      if (!prev) return null;
      return {
        ...prev,
        open: false,
        lastEventAt: ev.ts,
      };
  }
}
```

Key idea: **always compare `ev.ts` with `prev.lastEventAt`** before applying.

---

## 3. Treat Payloads as Patches

Never assume `payload` is complete.

* Only overwrite `severity` if a new one is provided.
* Only overwrite `message` if a new one is provided.
* Keep existing fields otherwise.

If you remember one rule:

> “No field resets to default just because a later event omitted it.”

---

## 4. Be Explicit About Channel

You have two reasonable strategies:

1. **Channel is immutable per `id`**:

   * On `open`: use `ev.channel`.
   * On `update`/`ack`/`close`: **ignore** `ev.channel` and keep `prev.channel`.

2. **Channel follows the latest event**:

   * On any event: if `prev` exists and `ev.channel !== prev.channel`, you intentionally switch.

Whichever you choose, do it **consistently**.
The rubric will reward clear, deliberate behavior, not silent drift.

---

## 5. Return a Stable Shape

Always return:

* An `SignalState[]` (possibly empty),
* With all required fields populated,
* In a predictable order (e.g. sorted by `id` or `lastEventAt`).

Example:

```ts
return Array.from(byId.values()).sort((a, b) => a.id.localeCompare(b.id));
```

Even if the spec doesn’t require ordering, having one makes debugging and testing easier, and often earns rubric credit.

---

## 6. Make It Easy to Test Locally

Before sending your solution to the boss, you can add a quick `selfTest`:

```ts
function selfTest() {
  const events: SignalEvent[] = [
    // add a few open/update/close/ack sequences here
  ];

  const result = computeSignalPanel(events);
  console.log(result);
}

// selfTest();
```

This is optional but powerful: it forces you to **think like a test** before the boss does.

---

> ELARA: "Once you can write reducers like this, most front-end state problems start looking like friendly prisms instead of chaos."
