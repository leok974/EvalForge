## Hint 1
Named exports let you export multiple values from a module:
```js
export function add(a, b) { return a + b; }
export const PI = 3.14159;
```
The grader checks that your file uses `export` (named or default).

## Hint 2
Default vs named exports:
```js
// Named export — import with curly braces
export function task() { ... }
import { task } from './main.js';

// Default export — import without curly braces
export default function task() { ... }
import task from './main.js';
```
The test file uses `import { task } from './main.js'`, so use a **named export**.
