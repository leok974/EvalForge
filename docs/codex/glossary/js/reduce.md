---
title: Reduce
id: glossary/js/reduce
world: js
level: intermediate
tags: [arrays, iteration, functional]
related:
  - codex:glossary/js/array
  - codex:glossary/js/map
  - codex:glossary/js/filter
---

# Reduce

## Definition
`Array.prototype.reduce()` combines array elements into a single value (like a sum, object, or grouped map). It repeatedly applies an accumulator function from left to right.

## Usage
- Sum numbers.
- Build lookup objects.
- Group items by a key.

## Example
```js
const nums = [1, 2, 3, 4];
const sum = nums.reduce((acc, n) => acc + n, 0); // 10

const words = ["a", "bb", "ccc"];
const byLen = words.reduce((acc, w) => {
  acc[w.length] = (acc[w.length] ?? 0) + 1;
  return acc;
}, {}); // { 1: 1, 2: 1, 3: 1 }
```

## Pitfalls

* Forgetting the initial value can cause edge-case bugs (especially with empty arrays).
* Complex reduces can be hard to read; consider `map` + `filter` + `reduce` or a loop.

## Related

* Array: reduce operates on arrays.
* Map: map transforms items; reduce combines them.
* Filter: filter selects items; reduce combines them.
