---
title: Map
id: glossary/js/map
world: js
level: beginner
tags: [arrays, iteration, functional]
related:
  - codex:glossary/js/array
  - codex:glossary/js/filter
  - codex:glossary/js/reduce
---

# Map

## Definition
`Array.prototype.map()` creates a **new array** by transforming each element of an existing array. It's used when you want to convert items 1:1 (same length, different values).

## Usage
- Convert data shapes (e.g., objects → strings).
- Transform values without mutating the original array.
- Chain with other array methods.

## Example
```js
const prices = [10, 20, 30];
const withTax = prices.map(p => p * 1.06); // [10.6, 21.2, 31.8]

const users = [{ name: "Leo" }, { name: "Kim" }];
const names = users.map(u => u.name); // ["Leo", "Kim"]
```

## Pitfalls

* `map` is for transforming; if you're not using the returned array, use `forEach`.
* Don't confuse `map()` with `Map` (the key/value collection type).

## Related

* Array: map operates on arrays.
* Filter: filter selects items; map transforms them.
* Reduce: reduce combines items; map transforms each item.
