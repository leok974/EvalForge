# Tutorial — React Ignition

## What You’ll Learn
- How to write a React component as a plain function
- How JSX maps to `React.createElement(type, props, children)`
- How tests inspect element type + children

## Approach
Your component should return a single React element created manually:

- `type` → `"div"`
- `props` → `{ "data-testid": "welcome" }`
- `children` → `"Hello React"`

The test finds the node by test id and asserts:
- `welcome.type === "div"`
- `welcome.children[0] === "Hello React"`

## Implementation Plan
1. **Open the entrypoint**
   - Edit `data/quests/react-ignition/workspace/task.mjs`.

2. **Export a named component**
   - Define `function App() { ... }`
   - Export it as a **named export** (`export function App() {}` or `export { App }`).

3. **Return the correct element**
   - Return `React.createElement("div", { "data-testid": "welcome" }, "Hello React")`.

4. **Quick structure sanity check**
   - Root element is a `div`.
   - Prop name is exactly `data-testid`.
   - Text matches exactly (including capitalization).

## Testing
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Pitfalls

* Accidentally using JSX (forbidden)
* Forgetting the `data-testid` prop or misspelling it
* Returning the right text but in the wrong place (test checks `children[0]`)
* Extra whitespace/newlines in the string

## Self-Check

* Does `App()` return a single `div` element?
* Does it include `{ "data-testid": "welcome" }`?
* Is the child string exactly `"Hello React"`?
