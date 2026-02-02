---
title: Intersection Types
id: typescript/intersection-types
---
# Intersection Types

Combining multiple types into one.

```typescript
type Draggable = { drag: () => void };
type Resizable = { resize: () => void };
type UIElement = Draggable & Resizable;
```
