# Hints — React Props: Dynamic Greeting

## Hint 1 (nudge)
Decide the displayed name first, then build the greeting string.

## Hint 2 (more specific)
The tests pass `{}` for the default case, so `props.name` will be `undefined`.

## Hint 3 (close)
Use a nullish check:
- `const name = props.name == null ? "Stranger" : props.name`
Then render:
- `React.createElement("h1", { "data-testid": "welcome" }, \`Hello, ${name}!\`)`
