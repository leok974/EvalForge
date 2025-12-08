# Boss: History Rewriter – Golden Git Incident Runbook

Scenario: Commit history has been mangled by a bad rebase/force-push on `feature/auth-redesign`, and a bug surfaced after the last deploy.

---

## Incident Context

- **Branches:**
  - `main` – production trunk.
  - `release/1.2` – release branch for current version.
  - `feature/auth-redesign` – long-lived feature branch for auth.

- **Symptoms:**
  - A regression in auth appears after the last deploy.
  - Some commits mentioned in older discussions no longer appear in `git log` on `feature/auth-redesign`.
  - There is evidence in chat that someone ran `git rebase main` on `feature/auth-redesign` and then `git push --force`.

**Goal:**  
Recover any lost work, identify the regression commit, and restore a safe, understandable history without breaking teammates’ clones.

---

## Phase 1 – Inspect & Map the Graph

1. **Fetch everything from origin**

```bash
git fetch --all --prune
```

2. **Draw a full graph view**

```bash
git log --oneline --graph --decorate --all | less
```

* Identify:

  * Tips of `origin/main`, `origin/release/1.2`, `origin/feature/auth-redesign`.
  * Any unusual split between local and remote branch tips.
  * Merge commits vs rebases (linear vs criss-cross history).

3. **Check for divergence between local and remote**

```bash
git branch -vv
```

* Note if local `feature/auth-redesign` diverges from `origin/feature/auth-redesign`.

4. **Snapshot current state**

Before changing anything, create a **safety branch**:

```bash
git checkout origin/main
git checkout -b rescue/pre-history-rewriter-$(date +%F)
```

This gives us a stable pointer to reconstruct from if we get lost.

---

## Phase 2 – Recovery Plan

### A. Use Reflog to Find Lost Commits

5. **Inspect reflog for feature branch**

```bash
git checkout feature/auth-redesign
git reflog --date=iso | less
```

* Look for entries around the time of the rebase/force-push:

  * Reflog entries like `rebase finished`, `checkout: moving from ...`, `reset: moving to ...`.

6. **Create a backup branch at the pre-rebase state**

When you find a reflog entry representing the old tip (e.g. `abc1234`):

```bash
git branch backup/auth-redesign-pre-rebase abc1234
```

Now we have a named branch preserving the original feature history.

### B. Compare Old vs New Feature History

7. **Compare commits between current and backup**

```bash
git log --oneline --graph backup/auth-redesign-pre-rebase..feature/auth-redesign
git log --oneline --graph feature/auth-redesign..backup/auth-redesign-pre-rebase
```

* Identify:

  * Commits present only in backup → potentially **lost** in rebased branch.
  * Commits present only in current branch → new work since rebase.

### C. Identify Regression Candidate

8. **Identify time window and candidate commits**

* From incident timeline (deploy time), narrow down to commits merged into `main` before the bug appeared:

```bash
git checkout main
git log --oneline --since="YYYY-MM-DD" --decorate
```

9. **Use git bisect (if symptom is testable)**

If we have a reliable failing test or repro script:

```bash
git bisect start
git bisect bad main
git bisect good <known-good-tag-or-commit>
# At each step:
#  - Run tests or repro script
#  - git bisect good / git bisect bad
```

At the end, record the culprit commit:

```bash
culprit=$(git rev-parse HEAD)
git bisect reset
echo "Culprit commit: $culprit"
```

---

## Phase 3 – Execute Safely

### A. Fixing Production (Public History)

10. **Avoid rewriting public history on main**

Instead of rewriting `main`, prefer a **revert** or forward-fix:

```bash
git checkout main
git revert <culprit-commit-sha>
# Resolve conflicts if any, then:
git commit
```

11. **Push the fix**

```bash
git push origin main
```

12. **Cherry-pick to release branch if needed**

```bash
git checkout release/1.2
git cherry-pick <revert-commit-sha>
git push origin release/1.2
```

### B. Cleaning up the Feature Branch (Optional / With Coordination)

If the team agrees to clean up `feature/auth-redesign`:

13. **Create a polished branch from recovered history**

```bash
git checkout backup/auth-redesign-pre-rebase
# Optionally rebase onto current main (private history):
git rebase main

git branch feature/auth-redesign-v2
git push origin feature/auth-redesign-v2
```

14. **Coordinate with the team**

* Announce in your channel:

  * Old branch: `feature/auth-redesign` had unsafe history.
  * New branch: `feature/auth-redesign-v2` is the clean version.
* Provide instructions for teammates to switch:

```bash
git fetch origin
git checkout feature/auth-redesign-v2
```

---

## Phase 4 – Verify & Communicate

15. **Verify the fix**

* Rerun tests for auth.
* Deploy to staging or canary.
* Confirm the bug is gone.

16. **Update documentation**

* Write a short internal postmortem:

  * What happened (bad rebase/force-push),
  * How we recovered (reflog, backup branch, revert),
  * Updated guidelines (no force-pushes to shared branches).

17. **Add guardrails**

* Add branch protection to `main` and `release/*`:

  * Require reviews.
  * Disallow force-pushes or direct commits.
* Update team Git guidelines with this runbook.

This runbook is **copy-paste safe**, backup-first, and favors reverting over rewriting for public branches, which is the expected “golden” behavior for the History Rewriter boss.
