# Path

## Definition
A **path** is an address to a file or directory. An **absolute path** starts with `/` (root-based). A **relative path** starts from your current working directory.

## Tiny example
Absolute: `/home/leo/projects/app`
Relative: `projects/app` (from `/home/leo`)

## Common pitfall
Confusing `/sandbox/demo` with `sandbox/demo`. The first is absolute; the second is relative. When in doubt, run `pwd` and print the full path.

## Related
Current Working Directory, Filesystem
