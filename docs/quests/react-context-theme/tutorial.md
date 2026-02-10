# Tutorial — React Context: Theme

## What You’ll Learn
- Creating a context with a default value
- Providing a value via a Provider
- Consuming a value via `useContext`

## Approach
There are two halves:
1) Provider: wrap children with `ThemeContext.Provider` and supply `value: theme`
2) Consumer: `useContext(ThemeContext)` to get the current theme string

The test renders a wrapper that nests:
`ThemeProvider(theme="dark")` → `ThemedButton`
So the button must read `"dark"` from context.

## Implementation Plan
1. Provider implementation:
   - Return `React.createElement(ThemeContext.Provider, { value: theme }, children)`
2. Consumer implementation:
   - `const theme = useContext(ThemeContext)`
   - Return `React.createElement("button", { "data-testid": "btn" }, theme)`

## Testing
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Pitfalls

* Returning `children` without wrapping provider (context value won’t change)
* Rendering the default theme instead of the provided theme
* Forgetting `data-testid="btn"`

## Self-Check

* With provider theme `"dark"`, button text is `"dark"`
* Without provider, button would show default (but tests use provider)
