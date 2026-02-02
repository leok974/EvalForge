# map

## Definition
`map` transforms each element in an array and returns a new array of the same length.

## Tiny example
```js
const doubled = [1, 2, 3].map((n) => n * 2); // [2, 4, 6]
```

## Common pitfall
`map` is not for filtering. If you return `undefined` for some elements, the array still keeps its length.

## Related
filter, reduce
