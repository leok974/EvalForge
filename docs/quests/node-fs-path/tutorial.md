# Tutorial — node-fs-path

## What You’re Practicing
- Using `node:fs/promises` for async IO
- Building paths safely with `path.join`
- Thinking in terms of `process.cwd()` (runtime context)

## Implementation Plan
1. Build an absolute path:
   - `const inputPath = path.join(process.cwd(), fileName)`
2. Read file:
   - `await fs.readFile(inputPath, "utf-8")`
3. Uppercase:
   - `const upper = content.toUpperCase()`
4. Write output in the same directory:
   - `const outPath = path.join(process.cwd(), "output.txt")`
   - `await fs.writeFile(outPath, upper, "utf-8")`

## Pitfalls
- forgetting `"utf-8"` (you’ll get a Buffer)
- writing output in the wrong directory
- using string concat instead of `path.join`
