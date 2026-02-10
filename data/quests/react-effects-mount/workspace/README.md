# React Effects: Mount/Unmount

Edit `task.mjs` to export a component `LifecycleLogger`.

Requirements:
1. Accept props `onMount` and `onUnmount` (functions).
2. Use `useEffect` to call `onMount` when the component mounts.
3. Return a cleanup function from the effect that calls `onUnmount`.
4. Render null or any element.
