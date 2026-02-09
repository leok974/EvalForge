---
title: Runtime and Process
id: glossary/node/runtime-and-process
world: node
---

# Runtime and Process

Content regarding the Node.js runtime and process object is currently under development.

Refer to official Node.js documentation for `process`.


## Pitfalls

- Blocking the event loop with heavy synchronous operations.
- Unhandled promise rejections can crash the process.

## Related

- [[node/event-loop]]
- [[node/modules]]

## Example

``` typescript
const example = () => {
  console.log('Hello');
};
```