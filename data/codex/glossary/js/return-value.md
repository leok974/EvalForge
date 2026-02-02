# return value

## Definition
The return value is the output a function produces using `return`. You can store it in a variable or pass it to other functions.

## Tiny example
```js
function double(x) { return x * 2; }
const y = double(5); // y is 10
```

## Common pitfall
Logging a value does not return it. If a validator expects a return value, use `return`.

## Related
function, console.log
