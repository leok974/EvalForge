---
title: Effects
id: glossary/react/effects
world: react
level: intermediate
tags: [react, side-effects, hooks]
related:
  - codex:glossary/react/state
  - codex:glossary/react/custom-hooks
  - codex:glossary/react/performance-basics
---

# Effects

## Definition
An **effect** is code that runs after React commits a render to the screen. `useEffect` is used for side effects: subscriptions, timers, network requests, and syncing with external systems.

## Usage
- Use effects to "connect" your component to the outside world.
- Return a cleanup function to unsubscribe/clear timers.
- Control when it runs using the dependency array.

## Example
```js
import React from "react";

function TitleSync(props) {
  React.useEffect(() => {
    document.title = props.title;
    return () => {
      // optional cleanup
    };
  }, [props.title]);

  return React.createElement("div", null, "Updated title");
}
```

## Pitfalls

* Missing dependencies can cause stale data bugs.
* Overusing effects for derived UI logic leads to unnecessary complexity.

## Related

* State: effects often sync state with external systems.
* Custom Hooks: effects are often wrapped in custom hooks.
* Performance Basics: effects can impact performance.