# callback

## Definition
A callback is a function passed into another function so it can be called later. With arrays, callbacks often run once per element.

## Tiny example
```js
[1, 2, 3].map((n) => n * 2);
```

## Common pitfall
If you use curly braces in an arrow callback, you must `return`:

```js
nums.map((n) => { return n * 2; });
```

## Related
function, map
