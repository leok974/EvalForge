# Filesystem and Paths

Reading and writing files is fundamental.

## Objective
Implement `processFile(fileName)` so it reads a file from the current working directory,
uppercases the content, and writes it to `output.txt`.

## Requirements
Implement `processFile(fileName)` in `utils.js`:

1) Read the file specified by `fileName` (assume it's in the current working directory).
2) Convert its content to **UPPERCASE**.
3) Write the result to a new file named `output.txt`.

## Tips
- Use `path.join(process.cwd(), fileName)` to construct a safe absolute path.
- Use `fs.readFile` / `fs.writeFile` from `node:fs/promises`.

## Success Criteria
Public tests pass.
