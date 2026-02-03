# Filesystem & Paths: Read/Write Without Pain

## Outcome

Read/write files using correct paths.

## Core concepts

`fs`, `path.join`, cwd, encoding.

## Mental model

always build paths intentionally; never assume cwd in prod.

## Walkthrough

read JSON file, write output file, handle missing file.

## Practice

implement a “copy template to output” task.

## Common pitfalls

Windows path separators, relative path surprises.

## Check yourself

What does `process.cwd()` represent?

