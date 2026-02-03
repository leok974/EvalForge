# Filesystem and Paths

Reading and writing files is fundamental.

## Goal
Implement `processFile(fileName)` in `utils.js`.
1.  Read the file specified by `fileName` (assume it's in the current working directory).
2.  Convert its content to **UPPERCASE**.
3.  Write the result to a new file named `output.txt`.

## Tips
- Use `path.join(process.cwd(), fileName)` to be safe.
- Use `fs.readFile` and `fs.writeFile` from `node:fs/promises`.
