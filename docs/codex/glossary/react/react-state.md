---
title: State
id: glossary/react/state
world: react
level: beginner
tags: [react, interactivity, hooks]
related:
  - codex:glossary/react/components
  - codex:glossary/react/effects
  - codex:glossary/react/controlled-inputs
---

# State

## Definition
**State** is data owned by a component that can change over time and trigger re-renders. In function components, state is managed with `useState`.

## Usage
- Use state for UI that changes (form inputs, toggles, fetched data).
- Keep state minimal and derived values computed during render.
- Update state with the setter function, not by mutating variables.

## Example
```js
import React from "react";

function Counter() {
  const [count, setCount] = React.useState(0);

  return React.createElement(
    "button",
    { onClick: () => setCount(count + 1) },
    `Count: ${count}`
  );
}
```

## Pitfalls

* Setting state during render causes infinite loops.
* Updating based on previous state should use the functional form: `setCount(c => c + 1)`.

## Related

* Components: components hold state.
* Effects: effects often depend on state.
* Controlled Inputs: inputs are driven by state.