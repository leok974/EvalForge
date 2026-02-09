---
title: Events
id: glossary/react/events
world: react
level: beginner
tags: [react, interactivity, dom]
related:
  - codex:glossary/react/controlled-inputs
  - codex:glossary/react/components
  - codex:glossary/react/performance-basics
---

# Events

## Definition
**Events** in React are how your UI responds to user interactions (click, input, submit). React normalizes events across browsers and delivers them through handler props like `onClick`.

## Usage
- Attach handlers to elements via props like `onClick`, `onChange`.
- Prevent default browser behavior when needed (`e.preventDefault()`).
- Keep handlers small; move logic into helper functions.

## Example
```js
import React from "react";

function Form() {
  function handleSubmit(e) {
    e.preventDefault();
    console.log("submitted");
  }

  return React.createElement(
    "form",
    { onSubmit: handleSubmit },
    React.createElement("button", { type: "submit" }, "Submit")
  );
}
```

## Pitfalls

* Forgetting `preventDefault()` in forms causes page reloads.
* Inline handlers that recreate functions every render can affect memoization (usually fine, but be aware).

## Related

* Controlled Inputs: events drive controlled inputs.
* Components: components handle events.
* Performance Basics: event handlers can be memoized.