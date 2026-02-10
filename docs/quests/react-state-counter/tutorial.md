# Tutorial — React State: Counter

## What You’ll Learn
- How to initialize component state with `useState`
- How to update state from button clicks
- How the rendered output updates after state changes

## Approach
You’ll keep a `count` state and render it in a `div`.
When the increment button is clicked, call `setCount`.
When reset is clicked, set it back to 0.

The test checks the rendered text inside the count div, so render `String(count)`.

## Implementation Plan
1. Ensure state exists:
   - `const [count, setCount] = useState(0)`
2. Render the count:
   - `React.createElement("div", { "data-testid": "count" }, String(count))`
3. Add handlers:
   - Increment: `onClick: () => setCount(c => c + 1)`
   - Reset: `onClick: () => setCount(0)`
4. Confirm button test IDs match exactly.

## Testing
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Pitfalls

* Forgetting `onClick` props (buttons won’t change state)
* Rendering the number without string conversion (some renderers may expose numbers)
* Updating state as `setCount(count + 1)` (works here, but functional update is safer)

## Self-Check

* Initial: `"0"`
* Click increment twice: `"2"`
* Click reset: `"0"`
