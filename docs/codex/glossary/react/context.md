---
title: Context
id: glossary/react/context
world: react
level: intermediate
tags: [react, state-management, global]
related:
  - codex:glossary/react/props
  - codex:glossary/react/state
  - codex:glossary/react/performance-basics
---

# Context

## Definition
**Context** is a way to pass values through the component tree without passing props manually at every level. It's useful for "app-wide" data like theme, auth user, or localization.

## Usage
- Create a context with a default value.
- Provide a value near the top with `<Provider>`.
- Read it in children with `useContext`.

## Example
```js
import React from "react";

const ThemeContext = React.createContext("dark");

function App() {
  return React.createElement(
    ThemeContext.Provider,
    { value: "light" },
    React.createElement(Panel)
  );
}

function Panel() {
  const theme = React.useContext(ThemeContext);
  return React.createElement("div", null, `theme=${theme}`);
}
```

## Pitfalls

* Context updates re-render all consumers; don't put rapidly-changing values in a single global context without care.
* Context is not a replacement for all state—use it for shared configuration or truly global data.

## Related

* Props: context avoids prop drilling.
* State: context often distributes state.
* Performance Basics: redundant context updates cause re-renders.