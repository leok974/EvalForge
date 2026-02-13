# P4 Git World Upgrade Plan

## Canonical Slugs (Training-Grade)
We are adopting the following 10 slugs for the Git World upgrade, replacing legacy content where necessary.

1. `git-ignition` (Init + First Commit)
2. `git-status-diff` (Status & Diff)
3. `git-add-commit` (Stage Selected)
4. `git-branches` (Create + Switch)
5. `git-merge-conflict` (Merge + Conflict Resolution)
6. `git-log` (History Report)
7. `git-undo-revert` (Revert)
8. `git-stash` (Stash & Pop)
9. `git-tags` (Annotated Tags)
10. `git-rebase-onto-main` (Rebase Feature)

## Changes from Legacy
- Removed `git-remote-push` (Network requirement removed).
- Renamed `git-init-clone` -> Covered by `ignition`.
- Renamed `git-branch-merge` -> Split/Refined into `git-branches` and `git-merge-conflict`.
- Renamed `git-tag-release` -> `git-tags`.
- Renamed `git-rebase-linear` -> `git-rebase-onto-main`.

## Verification
- Solution Mode: 10/10 PASS
- Student Mode: 0/10 PASS
