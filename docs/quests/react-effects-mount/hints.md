# Hints — React Effects: Mount/Unmount

## Hint 1 (nudge)
Effects run after rendering. Cleanup runs when the component is removed.

## Hint 2 (more specific)
Your effect should:
- call `onMount()` once
- return a function that calls `onUnmount()`

## Hint 3 (close)
```js
useEffect(() => {
  onMount?.();
  return () => onUnmount?.();
}, [onMount, onUnmount]);
```
