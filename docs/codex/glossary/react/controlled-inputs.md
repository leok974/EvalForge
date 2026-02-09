---
title: Controlled Inputs
id: glossary/react/controlled-inputs
world: react
level: intermediate
tags: [react, forms, state]
related:
  - codex:glossary/react/state
  - codex:glossary/react/events
---

# Controlled Inputs

## Definition
A **controlled input** is a form field whose value is driven by React state. The input displays the state value, and updates state on change.

## Usage
- Keep input value in `useState`.
- Bind `value` to state.
- Update state in `onChange`.

## Example
```js
import React from "react";

function NameField() {
  const [name, setName] = React.useState("");

  return React.createElement("input", {
    value: name,
    onChange: (e) => setName(e.target.value),
    placeholder: "Your name",
  });
}
```

## Pitfalls

* Mixing controlled and uncontrolled patterns (sometimes using `defaultValue`, sometimes `value`) can cause warnings and weird behavior.
* For expensive validation, debounce work instead of validating on every keystroke.

## Related

* State: controlled inputs are backed by state.
* Events: change events update state.