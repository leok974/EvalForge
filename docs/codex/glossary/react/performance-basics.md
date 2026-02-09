---
title: Performance Basics
id: glossary/react/performance-basics
world: react
level: intermediate
tags: [react, optimization, tuning]
related:
  - codex:glossary/react/lists-and-keys
  - codex:glossary/react/context
  - codex:glossary/react/effects
  - codex:glossary/react/props
---

# Performance Basics

## Definition
React performance is mostly about **avoiding unnecessary re-renders** and keeping rendering work small. Most apps are fast by default; optimize only when measurements show a real issue.

## Usage
- Keep component trees shallow and focused.
- Use stable keys for lists.
- Memoize expensive calculations (`useMemo`) and stable callbacks (`useCallback`) when it matters.
- Split state so changes don't re-render unrelated parts.

## Example
```js
import React from "react";

const Expensive = React.memo(function Expensive(props) {
  return React.createElement("div", null, props.value);
});
```

## Pitfalls

* Premature optimization adds complexity with little gain.
* `React.memo` / `useMemo` can hurt if dependencies churn every render.

## Related

* Lists and Keys: correct keys prevent re-renders.
* Context: optimize context to avoid global re-renders.
* Effects: avoid expensive effects.