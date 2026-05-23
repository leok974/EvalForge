---
title: Props
id: glossary/react/props
world: react
level: beginner
tags: [react, data-flow, fundamentals]
related:
  - codex:glossary/react/components
  - codex:glossary/react/context
  - codex:glossary/react/state
---

# Props

## Definition
**Props** (properties) are inputs passed from a parent component to a child. Props are read-only: a child should not mutate props, only use them to render.

## Usage
- Use props to configure a component (text, handlers, flags).
- Pass callbacks down to let children "request" changes.
- Prefer explicit props over hidden global state.

## Example
```js
import React from "react";

function Button(props) {
  return React.createElement(
    "button",
    { onClick: props.onClick, disabled: props.disabled },
    props.label
  );
}
```

## Pitfalls

* Mutating props breaks the mental model and can cause stale UI.
* Passing too many props through many layers can cause "prop drilling" (consider context).

## Related

* Components: components accept props.
* Context: context avoids prop drilling.
* State: props often come from parent state.