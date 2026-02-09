---
title: Custom Hooks
id: glossary/react/custom-hooks
world: react
level: intermediate
tags: [react, hooks, composition]
related:
  - codex:glossary/react/effects
  - codex:glossary/react/state
  - codex:glossary/react/performance-basics
---

# Custom Hooks

## Definition
A **custom hook** is a function that uses React hooks to package reusable stateful logic. Custom hooks let you share behavior without duplicating code or creating complex component hierarchies.

## Usage
- Name hooks with `useX`.
- Call hooks only at the top level (no loops/conditions).
- Return values/handlers for components to use.

## Example
```js
import React from "react";

function useToggle(initial = false) {
  const [on, setOn] = React.useState(initial);
  const toggle = () => setOn((v) => !v);
  return { on, toggle };
}
```

## Pitfalls

* Violating the Rules of Hooks (calling conditionally) breaks hook ordering.
* Custom hooks shouldn't hide important side effects—document what they do.

## Related

* Effects: custom hooks often wrap effects.
* State: custom hooks often encapsulate state.
* Performance Basics: custom hooks can encapsulate optimization.