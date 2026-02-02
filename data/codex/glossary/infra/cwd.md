# Current Working Directory (CWD)

## Definition
The **current working directory** is the directory your shell is “in.” Relative paths are interpreted from the CWD, and many commands (like `ls`) default to operating on the CWD.

## Tiny example
If `pwd` prints `/app`, then `cat config.json` refers to `/app/config.json`.

## Common pitfall
Running commands from the wrong directory causes confusing errors (missing files, wrong outputs). A good habit is:
- `pwd` when unsure
- `ls` to confirm you see the expected files

## Related
Path, Shell
