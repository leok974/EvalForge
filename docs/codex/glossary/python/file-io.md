---
title: File Input/Output (I/O)
---

# Definition
**File I/O** is the process by which a program reads data from or writes data to a file on the disk.

# Why It Matters
Without File I/O, a program's data is lost once it finishes running. Use files to:
- Persist user settings and application state.
- Process large datasets that don't fit in memory.
- Log system activity for later auditing.

# The Context Manager (`with`)
Always use the `with` statement when opening files. It ensures the file is closed automatically—even if an error occurs.

```python
# Writing to a file
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Line 1\n")
    f.writelines(["Line 2\n", "Line 3\n"])

# Reading from a file
try:
    with open("output.txt", "r") as f:
        content = f.read()
        print(content)
except FileNotFoundError:
    print("The file was not found!")
```

# File Modes
- `'r'`: Read (default). Fails if file doesn't exist.
- `'w'`: Write. Overwrites existing file or creates a new one.
- `'a'`: Append. Adds to the end of the file.
- `'b'`: Binary mode (for images/PDFs).

# In EvalForge
Many "Data Pipeline" quests require you to read raw logs and write processed summaries using standardized I/O patterns.
