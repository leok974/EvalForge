---
slug: boss-branch-keeper-attacks
boss_id: branch_keeper
tier: 2
world_id: world-timeline
tags:
  - boss
  - branch_keeper
  - attacks
  - git
title: "The Branch Keeper – Failure Patterns"
---

> ZERO: "Most broken repos started as 'I just ran merge and hoped.'"

Attack patterns:

1. **Divergent Branch – "Dual Timeline"**  
   - Feature branch and main have distinct commits.
   - Tests check if you pick an appropriate strategy (merge, rebase, or reset) and sequence.

2. **Dirty Worktree – "Uncommitted Drift"**  
   - Local changes + remote updates.
   - Plan must include stashing or committing before sync.

3. **Hotfix vs Feature – "Mis-tagged History"**  
   - Need to patch a release and also keep main moving.
   - Tests check if you create the right branches and tags.

4. **Conflict Resolution – "Timeline Fracture"**  
   - Simulated conflicts.
   - Planner must acknowledge conflict points and outline steps, not just pretend they don’t exist.
