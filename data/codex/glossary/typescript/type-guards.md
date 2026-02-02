---
title: Type Guards
id: typescript/type-guards
---
# Type Guards

Functions that return a type predicate.

```typescript
function isString(x: any): x is string {
  return typeof x === "string";
}
```
