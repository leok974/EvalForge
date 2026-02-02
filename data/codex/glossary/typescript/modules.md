---
title: Modules
id: typescript/modules
---
# Modules

TS uses ES Modules syntax.

```typescript
// math.ts
export const add = (a: number, b: number) => a + b;

// main.ts
import { add } from './math';
```
