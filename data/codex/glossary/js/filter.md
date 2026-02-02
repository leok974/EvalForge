# filter

## Definition
`filter` keeps only the elements that pass a condition (callback returns true) and returns a new array.

## Tiny example
```js
const evens = [1, 2, 3, 4].filter((n) => n % 2 === 0); // [2, 4]
```

## Common pitfall
Returning a number instead of a boolean can “work” but is unclear. Prefer explicit boolean conditions.

## Related
map, reduce
