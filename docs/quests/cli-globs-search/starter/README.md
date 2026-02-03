# Globs & Search

Edit task.sh so it creates:

1) outputs/error_count.txt
   - a single integer: number of lines containing `ERROR` across all .log files

2) outputs/error_files.txt
   - filenames (no directories) that contain at least one `ERROR`, sorted, one per line

Rules:
- Match `ERROR` exactly (case-sensitive).
- Use search tools (grep/find) rather than hardcoding.
