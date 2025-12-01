---
id: react-render-cycles
title: React Render Cycles & Effects
world: world-js
tier: 2
difficulty: intermediate
tags: [react, performance, hooks]
summary: >-
  Understanding when React updates the DOM and how to avoid infinite useEffect loops.
version: 1
last_updated: 2025-11-29
xp_reward: 100
prerequisites: []
stack: [react]
source: curated
trust_level: high
---

# Definition
> TL;DR: A render cycle happens whenever state or props change. `useEffect` runs *after* the paint. Most bugs come from synchronizing state manually instead of deriving it.

# The Golden Path (Best Practice)
Avoid `useEffect` for data transformation. Derive state during render.

```tsx
// ✅ Good: Derived State
function Cart({ items }) {
  // Calculated on the fly. No extra state variable. No effect.
  const total = items.reduce((sum, item) => sum + item.price, 0);
  
  return <div>Total: {total}</div>;
}
```

# Common Pitfalls (Anti-Patterns)

❌ **Redundant State Sync:**

```tsx
function Cart({ items }) {
  const [total, setTotal] = useState(0);

  // ❌ Triggers a second render unnecessarily
  useEffect(() => {
    setTotal(items.reduce((sum, i) => sum + i.price, 0));
  }, [items]);

  return <div>Total: {total}</div>;
}
```

# Trade-offs

  - ✅ **Derived State:** Simpler, fewer bugs, single source of truth.
  - ❌ **Performance:** Expensive calculations might need `useMemo`.

# Interview Questions

1.  Why does `useEffect` run twice in Strict Mode? (To flush out side-effect bugs).
2.  When does a cleanup function run? (Before the *next* effect runs, or on unmount).
