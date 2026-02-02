## Outcome
You will learn what branches are and how to use them to work on changes safely without disrupting your main line of development.

## Concept in 30 seconds
A branch is a movable label pointing to a commit. It lets you try changes in isolation. **HEAD** is “where you are right now.” When you create a branch and switch to it, new commits move that branch forward. Branching is how teams work on features and fixes without stepping on each other.

## Key terms
- **Branch**: A movable label pointing to a commit.
- **HEAD**: The current checkout (where your working tree is based).
- **Switch/Checkout**: Changing which branch/commit your working tree uses.
- **Merge**: Combining changes from one branch into another.
- **Main Branch**: The primary baseline branch (often named `main`).

## Walkthrough
1) Confirm your current state (`git status`) and current branch (`git branch`).
2) Create a new branch for your work.
3) Switch to that branch and make a small change.
4) Commit the change on the feature branch.
5) Switch back to the main branch and merge the feature branch.
6) Use **Run** to practice the sequence; **Submit** when your repo history reflects the required branch/merge state.

## Example implementation
A safe feature branch flow:

```bash
# See current branches (* marks current)
git branch

# Create and switch to a new branch
git switch -c feature/readme-update

# Make a change
echo "Notes" >> README.md

# Stage + commit on the feature branch
git add README.md
git commit -m "Update README with notes"

# Switch back to main
git switch main

# Merge the feature branch
git merge feature/readme-update
```

## Common mistakes
- **Forgetting to switch branches before editing** (you accidentally commit on main).
- **Creating a branch but not committing anything on it** (nothing to merge).
- **Confusing HEAD with a branch name** (HEAD points to your current checkout).
- **Trying to merge with uncommitted changes** (stash/commit first).
- **Deleting a branch before its work is merged** (you can lose the pointer).

## Check yourself
- What does a branch point to?
- What does HEAD represent?
- Why is a feature branch safer than committing directly to main?
