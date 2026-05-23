---
title: JSX
id: glossary/react/jsx
world: react
level: beginner
tags: [react, syntax, templating]
related:
  - codex:glossary/react/components
  - codex:glossary/react/props
  - codex:glossary/react/events
---

# JSX

## Definition
**JSX** is a syntax extension that looks like HTML inside JavaScript. It compiles to `React.createElement(...)` calls. JSX is optional—React works without it.

## Usage
- Use JSX to write UI more ergonomically.
- Know that JSX is just syntax sugar for element creation.
- In EvalForge React world, you may build elements without JSX to stay pure JS.

## Example
```js
// JSX (conceptual)
const el = <button disabled={true}>Save</button>;

// Compiles to:
const el2 = React.createElement("button", { disabled: true }, "Save");
```

## Pitfalls

* JSX is not HTML: attributes are camelCased (`className`, `htmlFor`).
* Returning multiple siblings requires a wrapper (`<>...</>` or a parent element).

## Related

* Components: components usually return JSX.
* Props: JSX syntax passes props.
* Events: JSX syntax attaches event handlers.