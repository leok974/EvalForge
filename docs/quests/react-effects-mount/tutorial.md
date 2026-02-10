# Tutorial — React Effects: Mount/Unmount

## What You’ll Learn
- How `useEffect` runs after initial render
- How to return a cleanup function
- How lifecycle behavior is tested without a browser

## Approach
Use a single effect that:
1) calls `onMount()` once on mount  
2) returns a cleanup function that calls `onUnmount()` on unmount

A dependency array ensures the mount call doesn’t repeat unnecessarily.

## Implementation Plan
1. Add `useEffect(() => { ... }, [onMount, onUnmount])`
2. Inside the effect:
   - Call `onMount()` (if provided)
   - Return `() => onUnmount()` (if provided)
3. Render `null` (simplest).

## Testing
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Pitfalls

* Forgetting to return cleanup (unmount won’t be handled)
* Calling `onUnmount` immediately (should only happen in cleanup)
* Omitting dependencies entirely if your environment re-renders with new props

## Self-Check

* Mount: `onMount` increments once
* Immediately after mount: `onUnmount` still zero
* Unmount (hidden/extra test): cleanup should call `onUnmount`
