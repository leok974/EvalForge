# Tutorial — React Components: Composition

## What You’ll Learn
- How to create small components and compose them together
- How nesting shows up in the rendered tree (and how tests verify it)
- How to render a component as a child of another component without JSX

## Approach
Think in layers:
- `CardBody` is the **inner** piece (simple div + text).
- `Card` is the **outer** shell (div + a child component inside).

The test searches for `"card-body"` *inside* the `"card"` node, so nesting is the whole point.

## Implementation Plan
1. **Implement `CardBody` first**
   - Return `React.createElement("div", { "data-testid": "card-body" }, "I am the body")`.

2. **Implement `Card` as the wrapper**
   - Return `React.createElement("div", { "data-testid": "card" }, React.createElement(CardBody))`.

3. **Sanity check nesting**
   - `Card` should render exactly one root `div`.
   - That div should contain the `CardBody` element.

## Testing
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Pitfalls

* Returning `null` from either component
* Rendering `CardBody` outside of the `card` div (must be nested)
* Misspelling `data-testid` or the test id values

## Self-Check

* Does `CardBody` render the exact text `"I am the body"`?
* Does `Card` render a `div` with `data-testid="card"`?
* Is `CardBody` a child of `Card` in the element tree?
