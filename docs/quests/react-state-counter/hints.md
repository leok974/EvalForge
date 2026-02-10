# Hints — React State: Counter

## Hint 1 (nudge)
You already have `useState(0)`. Now wire the UI to that state.

## Hint 2 (more specific)
The increment button needs an `onClick` that does `setCount(c => c + 1)`.

## Hint 3 (close)
Render the count as a string:
- `React.createElement("div", { "data-testid": "count" }, String(count))`
And add:
- increment: `{ "data-testid": "increment", onClick: ... }`
- reset: `{ "data-testid": "reset", onClick: () => setCount(0) }`
