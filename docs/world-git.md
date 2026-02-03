# world-git — Workflow Foundations (Student Guide)

Welcome to the Git world.

Git is a **time machine** for your code. If you learn the mental model and the recovery moves,
you can experiment fearlessly — and you’ll move faster in every other world (Node/Infra/Agents).

---

## How Git quests work (EvalForge style)

You’ll usually be asked to:
- create commits with exact contents
- branch + merge/rebase
- resolve conflicts
- undo changes correctly

Your goal is not “memorize commands”.
Your goal is: **always know where your changes are** (Working Tree / Index / HEAD).

---

## The 80/20 mental model

### Git has 3 “places” for your work
1) **Working Tree** — your files right now
2) **Staging Area (Index)** — what the next commit will include
3) **HEAD** — your current commit

If you’re stuck, run:
```bash
git status
```

It tells you where your changes are.

---

## Safe daily workflow

```bash
git switch -c feat/my-change
# edit files
git status
git add -p
git commit -m "feat: something"
git push -u origin feat/my-change
```

---

## Common pitfalls (and fixes)

### “I committed the wrong files”

Fix: use partial staging.

```bash
git reset    # unstages everything (keeps working changes)
git add -p   # stage only what you want
git commit
```

### “I need to undo a commit”

* Shared branch? use **revert**
* Local/private? use **reset**

Read: docs/codex/world-git/reset-vs-revert.md

### “I messed up rebase / lost commits”

Use reflog. It’s the recovery button.

```bash
git reflog
git reset --hard <sha>
```

### “Conflicts freak me out”

Conflicts are normal. You’re just choosing which lines should win.
Use:

* `git status` to see which files are conflicted
* resolve in editor
* `git add <file>`
* `git rebase --continue` or `git commit`

---

## Debugging checklist

1. `git status` — where are changes?
2. `git log --oneline --decorate -n 10` — what commit am I on?
3. `git diff` / `git diff --staged` — what exactly changed?
4. If panic: `git reflog` — where was I before?

---

## Where the Codex fits

Open:
`docs/codex/world-git/README.md`

It has the mental model, recovery rules, and command patterns.
