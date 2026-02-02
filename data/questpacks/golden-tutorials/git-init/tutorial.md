## Outcome
You will learn how to create a new Git repository, stage changes, and make your first commit so your work becomes a tracked history.

## Concept in 30 seconds
Git is a history machine for your project. Your files live in three “places”: the **Working Tree** (your current files), the **Staging Area** (what you plan to commit), and the **Repository** (the saved history). A **Commit** is a snapshot of your staged changes with a message explaining what changed and why.

## Key terms
- **Repository**: The Git database that stores history.
- **Working Tree**: Your current files on disk.
- **Staging Area**: The “pre-commit” area for selecting changes.
- **Commit**: A saved snapshot in history.
- **Commit Message**: The short explanation attached to a commit.

## Walkthrough
1) Initialize Git once in your project folder (`git init`).
2) Create or edit a file in the working tree.
3) Check what changed (`git status`).
4) Add changes to the staging area (`git add <file>`).
5) Confirm what is staged (`git status` or `git diff --staged`).
6) Create a commit with a clear message (`git commit -m "..."`).
7) Use **Run** to practice the command flow; **Submit** when your repo state matches the quest requirements.

## Example implementation
A minimal first commit flow:

```bash
# 1) Create a repo
git init

# 2) Create a file
echo "Hello, Git" > hello.txt

# 3) See changes
git status

# 4) Stage the file
git add hello.txt

# 5) Confirm staging
git status
git diff --staged

# 6) Commit
git commit -m "Add hello.txt with a greeting"
```

## Common mistakes
- **Forgetting `git add`** and committing nothing (commit will fail or be empty).
- **Staging too much at once** (use `git add <file>` instead of `git add .` if you want precision).
- **Vague commit messages** (“update”) that don’t describe the change.
- **Editing after staging** and forgetting to re-stage (your commit won’t include the latest edits).
- **Running Git commands from the wrong folder** (not inside the repo).

## Check yourself
- What’s the difference between the working tree and the staging area?
- What does a commit represent?
- Why should commit messages be specific?
