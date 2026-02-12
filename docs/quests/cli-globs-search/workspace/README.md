# Globs & Search

Edit `task.sh` so it creates:

1) `outputs/error_count.txt`
   - a single integer: the number of lines containing `ERROR` across all `fixtures/*.log` files

2) `outputs/error_files.txt`
   - basenames (no directories) of the `.log` files that contain at least one `ERROR`
   - sorted ascending
   - one filename per line

## Rules
- Match `ERROR` exactly (case-sensitive).
- Only consider files matching `fixtures/*.log`.
- Use search tools (`grep`, `find`) rather than hardcoding.
- No extra stdout/stderr.
- Exit code must be `0`.
