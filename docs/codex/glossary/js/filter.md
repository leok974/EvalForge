---
title: Filter
id: glossary/js/filter
world: js
level: beginner
tags: [arrays, iteration, functional]
related:
  - codex:glossary/js/array
  - codex:glossary/js/map
  - codex:glossary/js/reduce
---

# Filter

## Definition
`Array.prototype.filter()` creates a **new array** containing only elements that pass a test. It's used to remove items you don't want while keeping order.

## Usage
- Keep only items matching a condition.
- Remove null/empty entries.
- Select subset of data based on criteria.

## Example
```js
const nums = [1, -2, 3, 0];
const positives = nums.filter(n => n > 0); // [1, 3]

const users = [
  { name: "Leo", active: true },
  { name: "Kim", active: false }
];
const active = users.filter(u => u.active); // [{ name: "Leo", active: true }]
```

## Pitfalls

* `filter` returns a new array; it does not modify the original.
* If your predicate returns non-boolean, JS will coerce truthiness (can be surprising).

## Related

* Array: filter operates on arrays.
* Map: map transforms items; filter selects items.
* Reduce: reduce combines items; filter selects items.
