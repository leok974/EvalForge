---
title: Components
id: glossary/react/components
world: react
level: beginner
tags: [react, ui, fundamentals]
related:
  - codex:glossary/react/props
  - codex:glossary/react/state
  - codex:glossary/react/effects
---

# Components

## Definition
A **React component** is a reusable unit of UI. It's just a JavaScript function (or class) that returns a React element tree describing what should appear on screen.

## Usage
- Break UI into small, focused components.
- Pass data in via props.
- Keep components "pure" when possible: same inputs → same output.

## Example
```js
import React from "react";

function Greeting(props) {
  return React.createElement("h1", null, `Hello, ${props.name}!`);
}

// Usage:
// React.createElement(Greeting, { name: "Leo" })
```

## Pitfalls

* Doing side effects inside the render path (network calls, timers) causes repeated work and bugs.
* Components that do too much become hard to test and reuse.

## Related

* Props: components receive data via props.
* State: components manage internal state.
* Effects: components trigger side effects.