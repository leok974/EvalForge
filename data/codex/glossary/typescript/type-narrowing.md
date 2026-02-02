---
title: Type Narrowing
id: typescript/type-narrowing
---
# Type Narrowing

Refining a type within a conditional block.

```typescript
function printId(id: string | number) {
  if (typeof id === "string") {
    console.log(id.toUpperCase()); // id is string here
  }
}
```
