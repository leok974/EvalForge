# Approvals & Diffs

Safe agents propose changes as diffs first.

---

## Diff-first workflow

1) Generate a patch/diff
2) Summarize impact + risk
3) Ask for approval
4) Apply patch
5) Verify
6) Record rollback instructions

---

## What needs approval?

Examples:
- deleting files
- deployments
- database migrations
- pushing commits
- changing auth/security logic
- spending money (API calls, cloud resources)

---

## Rollback standard

Every applied change must have a rollback path:
- git revert / reset
- restore backup
- re-run migration down (if supported)
