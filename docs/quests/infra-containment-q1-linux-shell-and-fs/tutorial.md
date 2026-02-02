## Outcome
You will learn how to navigate the Linux shell and filesystem so you can confidently find files, inspect directories, and run commands in the right place.

## Concept in 30 seconds
A Linux shell is a command-line interface for interacting with your system. The filesystem is a tree of directories and files rooted at `/`. Your most important mental model is: “commands run from a **current working directory (CWD)**, and paths can be **absolute** (start with `/`) or **relative** (from the CWD).”

## Key terms
- **Shell**: The command-line program that runs your commands.
- **Filesystem**: The directory/file tree on disk.
- **Path**: An address to a file or directory.
- **Current Working Directory (CWD)**: The directory commands run from.
- **Permissions**: Rules that control who can read/write/execute files.

## Walkthrough
1) Print where you are (`pwd`) and list files (`ls`).
2) Change directories (`cd`) and re-check with `pwd`.
3) Create files/folders (`mkdir`, `touch`) and verify with `ls`.
4) View file contents (`cat`) to confirm what you created.
5) Use relative paths when you can; use absolute paths when you must.
6) Click **Run** to try commands and verify outputs; **Submit** when you can reproduce the required directory/file state.

## Example implementation
A quick filesystem tour:

```bash
pwd
ls

mkdir -p sandbox/demo
cd sandbox/demo

touch notes.txt
echo "hello" > notes.txt

ls
cat notes.txt

cd ..
pwd
```

## Common mistakes
- **Running commands in the wrong folder** (always pwd when confused).
- **Mixing up relative vs absolute paths** (cd sandbox vs cd /sandbox).
- **Forgetting that Linux paths are case-sensitive** (Notes.txt ≠ notes.txt).
- **Permission errors** when trying to execute or write (check ls -l).
- **Using rm without understanding what it removes** (be careful with deletes).

## Check yourself
- What’s the difference between an absolute and a relative path?
- Why does the current working directory matter?
- What do permissions control?
