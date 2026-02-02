# Permissions

## Definition
**Permissions** control who can read (`r`), write (`w`), or execute (`x`) a file or directory. Linux permissions are typically set for the owner, group, and others.

## Tiny example
`ls -l` might show:
`-rw-r--r--` for a file (owner can read/write; others read only).

## Common pitfall
A script can fail with “Permission denied” if it isn’t executable. Fix with:
`chmod +x script.sh`
Also note: directories need execute permission to be “entered” with `cd`.

## Related
Filesystem, Path
