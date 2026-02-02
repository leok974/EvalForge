# reduce

## Definition
`reduce` combines an array into a single value using an accumulator (`acc`). Each step updates the accumulator.

## Tiny example
```js
const sum = [1, 2, 3].reduce((acc, n) => acc + n, 0); // 6
```

## Common pitfall
Forgetting the initial value causes edge-case bugs, especially for empty arrays. For sums, start with `0`.

## Related
map, filter
