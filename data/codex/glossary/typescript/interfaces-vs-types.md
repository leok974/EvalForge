---
title: Interfaces vs Types
id: typescript/interfaces-vs-types
---
# Interfaces vs Types

Two ways to define object shapes.

## Interface
Better for objects and extension.
```typescript
interface User {
  name: string;
}
```

## Type Alias
Better for unions and primitives.
```typescript
type ID = string | number;
```
