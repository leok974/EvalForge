# Tutorial — React Conditional Render

## What You’ll Learn
- How conditional rendering changes the element tree
- How to include/exclude elements using ternaries
- How tests check for elements by type (`findByType`)

## Approach
Return a wrapper element (often a `div`) containing:
- an `h2` always
- a `p` only when `isVisible` is true

In React, rendering `null` means “render nothing” — which is perfect for the hidden case.

## Implementation Plan
1. Keep the existing `h2` creation.
2. Add a conditional child:
   - if `isVisible` → `React.createElement("p", null, "Now you see me")`
   - else → `null`
3. Ensure both children are passed to the wrapper as separate arguments.

## Testing
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Pitfalls

* Always rendering a `p` with empty text (still counts as a `p`)
* Forgetting to pass the `p` as a child of the wrapper
* Misspelling the exact text `"Now you see me"`

## Self-Check

* Visible true: `h2` exists and `p` exists
* Visible false: `h2` exists and `p` does not exist
