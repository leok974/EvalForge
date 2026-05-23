---
title: Lists and Keys
id: glossary/react/lists-and-keys
world: react
level: beginner
tags: [react, rendering, arrays]
related:
  - codex:glossary/react/components
  - codex:glossary/react/performance-basics
---

# Lists and Keys

## Definition
When rendering a list, React needs a **key** for each item so it can track identity between renders. Keys help React apply minimal changes and preserve state correctly.

## Usage
- Use stable, unique keys (IDs from data).
- Keys must be unique among siblings.
- Avoid array index keys when items can reorder or be inserted.

## Example
```js
import React from "react";

function TodoList(props) {
  return React.createElement(
    "ul",
    null,
    props.todos.map((t) =>
      React.createElement("li", { key: t.id }, t.text)
    )
  );
}
```

## Pitfalls

* Using index as key can cause state/DOM mismatches when the list changes.
* Keys are not passed as props; they are only for React's internal diffing.

## Related

* Components: lists render components.
* Performance Basics: keys are critical for list performance.