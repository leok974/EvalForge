# Hints — React Ignition

## Hint 1 (nudge)
Build the element explicitly: **type + props + children**.

## Hint 2 (more specific)
The test asserts:
- `welcome.type` is `"div"`
- `welcome.children[0]` is `"Hello React"`

So your component must return a `div` whose first child is that exact string.

## Hint 3 (close)
Return this from `App`:
- `React.createElement("div", { "data-testid": "welcome" }, "Hello React")`
