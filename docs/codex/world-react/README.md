---
title: "World React — Codex"
world_id: world-react
type: codex_landing
version: 1
---

# World React — Codex (UI Foundations)

This Codex is your **reference hub** for React in EvalForge.  
React quests fail most often due to **mental model gaps** (state, rendering, effects) and **tiny correctness rules** (keys, dependencies, controlled inputs).

Use this page as your **map + debugger**.

---

## How to use this Codex

- **Learning mode:** skim “Core Model” → “Common Pitfalls” once.
- **Stuck mode:** jump to “Quest Map” and open the concept you’re currently using.
- **Debug mode:** go straight to the “Diagnostics Checklist”.

> Rule of thumb: If UI looks right but tests fail, it’s usually **state updates**, **render timing**, **effect dependencies**, or **DOM structure/labels**.

---

## The Core Model (the 80/20)

### 1) Render is a pure function of state + props
React calls your component function to produce UI.  
If you need data to persist across renders, it must live in **state** or **refs**.

### 2) State updates schedule re-renders
`setState(...)` does not update immediately — it schedules a render.
Use the **functional form** when next state depends on previous state:
```js
setCount((c) => c + 1)
```

### 3) Effects run after paint (mostly)

`useEffect` runs after React commits the DOM.
Treat it as: “sync React with the outside world” (fetch, timers, subscriptions).

### 4) Lists need stable keys

Keys tell React which item is which across renders.
Bad keys cause weird UI and failing tests.

---

## Quick Links (most-used concepts)

### Components & JSX

* [Components](./components.md) (props, children, composition)
* [Conditional rendering](./jsx.md)
* [Rendering lists](./lists-and-keys.md)

### State & events

* [`useState`](./state.md)
* [Event handlers](./events.md) (click, change, submit)
* [Controlled vs uncontrolled inputs](./controlled-inputs.md)

### Effects & async

* [`useEffect`](./effects.md) dependency arrays
* Fetching / loading states
* Cleanup (timers, subscriptions)

### Data flow patterns

* [Lifting state up](./context.md)
* Derived state (compute, don’t store)
* Memoization basics ([`useMemo`, `useCallback`](./performance-basics.md)) — only when necessary

### Testing-focused React

* Accessible queries (labels, roles)
* Stable selectors (`data-testid` only when needed)
* Deterministic rendering (avoid random IDs/time)

---

## React Quest Map (by concept)

> Map your current task to the concept area below.

### React basics & composition

* **react-ignition** → JSX, components, props, basic render contracts
* **react-components-props** → passing data, children, default props patterns

### State & interactivity

* **react-state** → `useState`, re-render mental model
* **react-events** → handlers, event payloads, state updates
* **react-forms** → controlled inputs, validation, submit patterns

### Lists & conditional UI

* **react-lists-keys** → keys, map rendering, empty states
* **react-conditional** → loading/error/empty branches

### Effects & async workflows

* **react-effects** → dependencies, cleanup
* **react-fetching** → loading state, abort patterns (or ignore-stale response)
* **react-performance-basics** (optional) → avoid unnecessary state, memoization in moderation

### App structure & integration (later)

* **react-routing** → route params, nested routes, deep links
* **react-state-architecture** → lifting state, context basics

*(If your quest slugs differ, keep the headings and swap the bullets — the structure is the value.)*

---

## Common Pitfalls (and why they happen)

### A) “State didn’t update”

Because React batches updates and schedules renders.
Fix: use functional updates when deriving from previous state.

```js
setItems((xs) => [...xs, newItem])
```

### B) “My effect runs too often / infinite loop”

Because dependencies change every render (objects/functions) or you update state unconditionally.
Fix: keep deps stable; compute inside effect; guard state updates.

```js
useEffect(() => {
  if (!id) return;
  // fetch...
}, [id]);
```

### C) “List UI glitches”

Because keys aren’t stable or you used array index.
Fix: use stable IDs.

```js
items.map((item) => <Row key={item.id} ... />)
```

### D) “Form input won’t type”

Because you made it controlled but didn’t update state onChange.
Fix:

```js
<input value={name} onChange={(e) => setName(e.target.value)} />
```

### E) “Tests can’t find elements”

Because semantics/accessibility are missing (labels, roles).
Fix: label inputs and buttons; prefer proper elements.

* Use `<button>` not `<div onClick>`
* Use `<label htmlFor="email">Email</label>` + `<input id="email" ...>`

---

## Diagnostics Checklist (when tests fail)

### 1) DOM correctness (most common)

* Are you using the correct element types (`button`, `input`, `form`)?
* Do elements have accessible names (label text, button text)?
* Are you rendering the expected text exactly (spacing/casing)?

### 2) State correctness

* Are you mutating state instead of creating new arrays/objects?

  * ❌ `items.push(x)` then `setItems(items)`
  * ✅ `setItems((xs) => [...xs, x])`
* Are you using functional updates when needed?

### 3) Effect correctness

* Is your dependency array correct?
* Are you updating state in an effect with no guard?
* Are you cleaning up timers/subscriptions?

### 4) Timing / async

* Are you setting loading state?
* Are you handling “stale response” (new request finishes after old)?
* Are you relying on `Date.now()` / randomness that makes tests flaky?

### 5) Keys & list identity

* Keys stable and unique?
* Avoid index keys unless list is static and never reorders.

---

## Tiny Patterns (copy/paste friendly)

### State updates (safe)

```js
setCount((c) => c + 1);
setItems((xs) => xs.filter((x) => x.id !== id));
setItems((xs) => [...xs, newItem]);
```

### Controlled input

```js
const [value, setValue] = useState("");
return <input value={value} onChange={(e) => setValue(e.target.value)} />;
```

### Submit handler

```js
function onSubmit(e) {
  e.preventDefault();
  // validate, then update state
}
return <form onSubmit={onSubmit}>...</form>;
```

### Effect for fetch (basic)

```js
useEffect(() => {
  let alive = true;
  async function run() {
    setStatus("loading");
    try {
      const res = await fetch(url);
      const data = await res.json();
      if (!alive) return;
      setData(data);
      setStatus("ok");
    } catch {
      if (!alive) return;
      setStatus("error");
    }
  }
  run();
  return () => { alive = false; };
}, [url]);
```

### Conditional UI (recommended)

```js
if (status === "loading") return <p>Loading...</p>;
if (status === "error") return <p>Error</p>;
if (!data?.length) return <p>No results</p>;
return <List data={data} />;
```

---

## Recommended expansions (future-proof hooks)

Tier-2 React can safely add:

* Context basics (when lifting state becomes painful)
* Custom hooks for reuse
* Better async patterns (AbortController)
* Component testing discipline (roles, labels, deterministic UI)

But Tier-1 should master: **render + state + events + lists + effects**.

---

### Tip: React success in EvalForge

When unsure, optimize for:

* **accessibility** (labels, roles, semantic tags)
* **deterministic output** (no randomness, stable keys)
* **simple state** (derive, don’t duplicate)
