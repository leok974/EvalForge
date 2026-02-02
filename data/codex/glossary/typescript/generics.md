---
title: Generics
id: typescript/generics
---
# Generics

Reusable types that work with any data type.

```typescript
function wrap<T>(value: T): T[] {
  return [value];
}
const nums = wrap<number>(10);
```
