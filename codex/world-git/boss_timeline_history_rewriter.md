# Boss Codex – History Rewriter

- **Boss ID:** `boss-timeline-history-rewriter`
- **World:** `world-git` – The Timeline
- **Track:** `timeline-commit-branch`
- **Stage:** `stage-1-timeline-commit`
- **Title:** History Rewriter
- **Tier:** Commit & Branch Boss (Stage 1 Capstone)

---

## Lore

The Timeline is not a straight line. It loops, branches, and sometimes breaks.

Deep within it walks the **History Rewriter**.

It has watched engineers:

- force-push over teammates’ work,
- lose entire features to a bad rebase,
- “fix” production by rewriting public history.

To pass, you must prove you can **reshape history without destroying it**:

- read complex commit graphs,
- design safe branch workflows,
- recover from disaster using the Timeline itself.

---

## Attacks

### 1. Detached Head

- **Symptom:** You checkout a commit, make changes, and suddenly you’re lost.
- **In game:** The boss presents a detached HEAD state with untracked work.
- **What it tests:** Understanding of HEAD, branches, and how to safely anchor work.

---

### 2. Merge Maelstrom

- **Symptom:** Multiple long-lived branches merge into main with conflicts and regressions.
- **In game:** A tangled graph with overlapping feature and hotfix branches.
- **What it tests:** Ability to interpret complex history and choose merge vs rebase strategies.

---

### 3. Rebase Roulette

- **Symptom:** A rebase goes wrong and commits “disappear”.
- **In game:** The boss shows a history where `git log` no longer shows a key feature branch.
- **What it tests:** Use of `git reflog`, backup branches, and safe recovery patterns.

---

### 4. Phantom Commits

- **Symptom:** A bug appears after “the last deploy”, but the culprit commit isn’t obvious.
- **In game:** The boss gives a failing test / symptom with many potential causes.
- **What it tests:** Use of `git bisect` and systematic debugging via history.

---

## Strategy

To defeat the History Rewriter, the player must demonstrate:

1. **Graph Literacy**
   - Comfort reading `git log --oneline --graph --all`.
   - Ability to summarize the story of a branch: where it diverged, what merged when.

2. **Safe History Editing**
   - Knows when to use `merge` vs `rebase` vs `revert`.
   - Always creates backup branches before destructive operations.
   - Distinguishes **public** vs **private** history.

3. **Recovery Skills**
   - Uses `git reflog` to find lost commits.
   - Uses `git bisect` to isolate regressions.
   - Leaves the repository in a clean, understandable state.

4. **Runbook Mindset**
   - Writes clear, copy-paste-safe sequences of commands.
   - Explains why each operation is chosen.
   - Never asks a tired teammate to type `git reset --hard` into production without backups.

---

## Boss Fight Shape

- **Submission Format:** A markdown **“Git Incident Runbook”** with sections:

  - `## Incident Context`
  - `## Phase 1 – Inspect & Map the Graph`
  - `## Phase 2 – Recovery Plan`
  - `## Phase 3 – Execute Safely`
  - `## Phase 4 – Verify & Communicate`

- **Scenario encoded for the player:**

  - Repo with:
    - `main`
    - `feature/auth-redesign`
    - `release/1.2`

  - Problems:
    - Someone rebased `feature/auth-redesign` onto `main` and force-pushed.
    - A bug surfaced after the last deploy (likely in auth).
    - Some commits seem “missing” from `feature/auth-redesign` and `main`.

The correct submission:

- Maps the current graph,
- Recovers lost work via `reflog`/backup branches,
- Suggests a safe fix (e.g., revert or forward-fix) instead of rewriting public history,
- Shows how to bisect to confirm the culprit commit.
