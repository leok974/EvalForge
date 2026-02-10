# Tutorial — React Props: Dynamic Greeting

## What You’ll Learn
- How props are passed into a component
- How to render conditional text based on a prop
- How tests validate text output exactly

## Approach
You only need two cases:
- `name` is **not** `null`/`undefined` → use it
- `name` is `null` or `undefined` → default to `"Stranger"`

Use `name == null` as the clean “missing” check.

## Implementation Plan
1. Export `Welcome(props)`
2. Compute `displayName`:
   - if `props.name == null` → `"Stranger"`
   - else → `props.name`
3. Return:
   - `React.createElement("h1", { "data-testid": "welcome" }, \`Hello, ${displayName}!\`)`

## Testing
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Pitfalls

* Using a falsy check (`if (!name)`) which incorrectly treats `""` as missing
* Missing punctuation: must include comma and exclamation point exactly
* Wrong element type (must be `h1`)

## Self-Check

* With `{ name: "Alice" }` → `"Hello, Alice!"`
* With `{}` → `"Hello, Stranger!"`
