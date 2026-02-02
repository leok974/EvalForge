---
title: Async & Promises
id: javascript/async
---
# Asynchronous JS

Handle operations that take time.

## Promises
Objects representing future value.

## Async/Await
Modern syntax for promises.
```javascript
async function getData() {
  const res = await fetch('/api');
  const data = await res.json();
}
```
