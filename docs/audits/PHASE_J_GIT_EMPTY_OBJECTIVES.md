# Phase J: Git Empty Objectives Audit

## Classification

Found 9 active Git quests (from `git_core.json`) with no/empty objectives.
5 additional "zombie" slugs (`git-tags`, `git-log`, `git-rebase-onto-main`, `git-merge-conflict`, `git-branches`) were identified but are **not referenced by any questpack** — ignored.

## Quest Status After Phase J

| Slug | Source | Had Golden State | Action Taken | Result |
|---|---|---|---|---|
| `git-add-commit` | `docs/quests` | ❌ | Captured state + injected objectives | ✅ Done |
| `git-branch-merge` | `docs/quests` | ❌ | Created solution + captured state + injected | ✅ Done |
| `git-init-clone` | `docs/quests` | ✅ (old format) | Re-captured in new format + injected | ✅ Done |
| `git-rebase-linear` | `docs/quests` | ❌ | Created solution + captured state + injected | ✅ Done |
| `git-remote-push` | `docs/quests` | ❌ | Created solution + captured state + injected | ✅ Done |
| `git-stash` | `docs/quests` | ❌ | Captured state + injected objectives | ✅ Done |
| `git-status-diff` | `docs/quests` | ❌ | Captured state + injected objectives | ✅ Done |
| `git-tag-release` | `docs/quests` | ❌ | Created workspace + solution + captured + injected | ✅ Done |
| `git-undo-revert` | `docs/quests` | ❌ | Captured state + injected objectives | ✅ Done |

## Verification Results

- **Drift Check**: `upgrade_objectives_state.py --check` → **PASS** (0 drift)
- **Git quests in certification failures**: **0** ✅
- **Objective kinds injected**: `fs_snapshot`, `git_status_clean`, `git_log_contains`

## Root Cause (Why They Were Empty)

The 9 Git quests had `quest.json` files with no `objectives` field. Phase I's normalizer
(`backfill_objectives_legacy.py`) only targeted quests with **invalid** objectives (e.g. `obj_default`),
not quests with **missing** objectives entirely. The scanner also treated `None` and `[]` identically
as "no objectives" but did not block certification on them — this has now been surfaced as a gap.

## Remaining Certification Failures (Out of Scope for Phase J)

These are pre-existing issues in other worlds:
- **9 invalid schemas**: SQL/Infra quests (legacy `obj_default` variants)
- **42 no objectives**: CLI (10), CSS (10), HTML (10), Node (10), React (2) worlds
- **76 missing golden**: Various worlds

These require a Phase K (CLI/CSS/HTML/Node/React backfill).
