import json
import os
from pathlib import Path

# User Specs
QUESTS_SPECS = [
    {
        "slug": "git-ignition",
        "title": "Git Ignition: Init + First Commit",
        "student_task_summary": "Create a fresh git repo, make one commit, and write repo state to outputs.",
        "requirements": [
            "Create outputs/ directory",
            "Create fresh repo at tmp/repo",
            "Initialize repo with default branch main",
            "Create file `hello.txt` with `Hello, EvalForge!` + newline",
            "Commit `chore: initial commit`",
            "Write outputs/state.txt: BRANCH=main, COMMITS=1, FILES=hello.txt"
        ],
        "test_code": """
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";
import path from "node:path";
import fs from "node:fs";

test("git-ignition: init + commit", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    // Check outputs/state.txt
    const state = readText(WS, "outputs/state.txt").trim();
    const expected = "BRANCH=main\\nCOMMITS=1\\nFILES=hello.txt";
    assert.strictEqual(state, expected, "outputs/state.txt mismatch");
});
""",
        "solution_sh": """#!/bin/sh
set -e
mkdir -p outputs
rm -rf tmp/repo
mkdir -p tmp/repo
cd tmp/repo
git -c init.defaultBranch=main init -q
echo "Hello, EvalForge!" > hello.txt
git add hello.txt
git -c user.name="EvalForge" -c user.email="evalforge@example.com" commit -q -m "chore: initial commit" --no-gpg-sign

# Generat output
echo "BRANCH=$(git branch --show-current)" > ../../outputs/state.txt
echo "COMMITS=$(git rev-list --count HEAD)" >> ../../outputs/state.txt
echo "FILES=$(ls)" >> ../../outputs/state.txt
"""
    },
    {
        "slug": "git-status-diff",
        "title": "Status & Diff: Detect Changes",
        "student_task_summary": "Report status metrics and diff summary.",
        "test_code": """
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-status-diff", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    const status = readText(WS, "outputs/status.txt").trim();
    assert.strictEqual(status, "STAGED=1\\nMODIFIED=0\\nUNTRACKED=1", "status.txt mismatch");
    
    const diff = readText(WS, "outputs/diff.txt").trim();
    assert.strictEqual(diff, "app.txt: v1 -> v2", "diff.txt mismatch");
});
""",
        "solution_sh": """#!/bin/sh
set -e
mkdir -p outputs
rm -rf tmp/repo
# Setup
mkdir -p tmp/repo && cd tmp/repo
git -c init.defaultBranch=main init -q
echo "v1" > app.txt
git add app.txt
git -c user.name="EF" -c user.email="ef@ex" commit -q -m "chore: baseline" --no-gpg-sign
# Changes
echo "v2" > app.txt
echo "draft" > notes.txt
git add app.txt
# Report
STAGED=$(git diff --cached --name-only | wc -l | tr -d ' ')
MODIFIED=$(git diff --name-only | wc -l | tr -d ' ')
UNTRACKED=$(git ls-files --others --exclude-standard | wc -l | tr -d ' ')
echo "STAGED=$STAGED" > ../../outputs/status.txt
echo "MODIFIED=$MODIFIED" >> ../../outputs/status.txt
echo "UNTRACKED=$UNTRACKED" >> ../../outputs/status.txt
echo "app.txt: v1 -> v2" > ../../outputs/diff.txt
"""
    },
    {
        "slug": "git-add-commit",
        "title": "Add + Commit: Stage Selected Files",
        "student_task_summary": "Stage specific files and commit them.",
        "test_code": """
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-add-commit", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    const out = readText(WS, "outputs/commit.txt").trim();
    assert.strictEqual(out, "HEAD=feat: add keep and readme\\nTRACKED=2\\nUNTRACKED=1");
});
""",
        "solution_sh": """#!/bin/sh
set -e
mkdir -p outputs
rm -rf tmp/repo
# Setup
mkdir -p tmp/repo && cd tmp/repo
git -c init.defaultBranch=main init -q
# Create files
echo "keep" > keep.txt
echo "skip" > skip.txt
echo "readme" > readme.md
# Stage specific
git add keep.txt readme.md
# Commit
git -c user.name="EF" -c user.email="ef@ex" commit -q -m "feat: add keep and readme" --no-gpg-sign
# Report
HEAD=$(git log -1 --pretty=%s)
TRACKED=$(git ls-files | wc -l | tr -d ' ')
UNTRACKED=$(git ls-files --others --exclude-standard | wc -l | tr -d ' ')
echo "HEAD=$HEAD" > ../../outputs/commit.txt
echo "TRACKED=$TRACKED" >> ../../outputs/commit.txt
echo "UNTRACKED=$UNTRACKED" >> ../../outputs/commit.txt
"""
    },
    {
        "slug": "git-branches",
        "title": "Branches: Create + Switch + Verify HEAD",
        "student_task_summary": "Create and switch branches.",
        "test_code": """
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-branches", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    const out = readText(WS, "outputs/branches.txt").trim();
    assert.strictEqual(out, "CURRENT=main\\nMAIN_HEAD=chore: base\\nFEATURE_HEAD=feat: ui tweak");
});
""",
        "solution_sh": """#!/bin/sh
set -e
mkdir -p outputs
rm -rf tmp/repo
# Setup
mkdir -p tmp/repo && cd tmp/repo
git -c init.defaultBranch=main init -q
echo "base" > app.txt
git add app.txt
git -c user.name="EF" -c user.email="ef@ex" commit -q -m "chore: base" --no-gpg-sign
# Feature branch
git branch feature/ui
git switch feature/ui
echo "ui" > app.txt
git add app.txt
git -c user.name="EF" -c user.email="ef@ex" commit -q -m "feat: ui tweak" --no-gpg-sign
# Switch back
git switch main
# Report
CURRENT=$(git branch --show-current)
MAIN_HEAD=$(git log -1 --pretty=%s main)
FEATURE_HEAD=$(git log -1 --pretty=%s feature/ui)
echo "CURRENT=$CURRENT" > ../../outputs/branches.txt
echo "MAIN_HEAD=$MAIN_HEAD" >> ../../outputs/branches.txt
echo "FEATURE_HEAD=$FEATURE_HEAD" >> ../../outputs/branches.txt
"""
    },
    {
        "slug": "git-merge-conflict",
        "title": "Merge: Resolve a Simple Conflict",
        "student_task_summary": "Merge branches and resolve conflict.",
        "test_code": """
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-merge-conflict", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    const out = readText(WS, "outputs/merge.txt").trim();
    assert.strictEqual(out, "STATUS=OK\\nHEAD=merge: feature/a\\nCONFIG=MODE=main+feature");
});
""",
        "solution_sh": """#!/bin/sh
set -e
mkdir -p outputs
rm -rf tmp/repo
# Setup
mkdir -p tmp/repo && cd tmp/repo
git -c init.defaultBranch=main init -q
# Base
echo "MODE=base" > config.txt
git add config.txt
git -c user.name="EF" -c user.email="ef@ex" commit -q -m "chore: base config" --no-gpg-sign
# Feature
git branch feature/a
git switch feature/a
echo "MODE=feature" > config.txt
git add config.txt
git -c user.name="EF" -c user.email="ef@ex" commit -q -m "feat: feature mode" --no-gpg-sign
# Main divergence
git switch main
echo "MODE=main" > config.txt
git add config.txt
git -c user.name="EF" -c user.email="ef@ex" commit -q -m "chore: main mode" --no-gpg-sign
# Merge (will fail)
git merge feature/a || true
# Resolve
echo "MODE=main+feature" > config.txt
git add config.txt
git -c user.name="EF" -c user.email="ef@ex" commit -q --no-edit --no-gpg-sign -m "merge: feature/a"
# Report
HEAD=$(git log -1 --pretty=%s)
CONFIG=$(cat config.txt)
echo "STATUS=OK" > ../../outputs/merge.txt
echo "HEAD=$HEAD" >> ../../outputs/merge.txt
echo "CONFIG=$CONFIG" >> ../../outputs/merge.txt
"""
    },
    {
        "slug": "git-log",
        "title": "Log: Produce History Report",
        "student_task_summary": "Generate history log.",
        "test_code": """
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-log", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    const out = readText(WS, "outputs/history.txt").trim();
    const expected = "1 chore: init\\n2 feat: add api\\n3 fix: handle null\\n4 docs: update readme";
    assert.strictEqual(out, expected);
});
""",
        "solution_sh": """#!/bin/sh
set -e
mkdir -p outputs
rm -rf tmp/repo
mkdir -p tmp/repo && cd tmp/repo
git -c init.defaultBranch=main init -q
# 4 commits
git -c user.name="EF" -c user.email="ef@ex" commit --allow-empty -q -m "chore: init" --no-gpg-sign
git -c user.name="EF" -c user.email="ef@ex" commit --allow-empty -q -m "feat: add api" --no-gpg-sign
git -c user.name="EF" -c user.email="ef@ex" commit --allow-empty -q -m "fix: handle null" --no-gpg-sign
git -c user.name="EF" -c user.email="ef@ex" commit --allow-empty -q -m "docs: update readme" --no-gpg-sign
# Log
git log --reverse --pretty=format:"%s" | awk '{print NR " " $0}' > ../../outputs/history.txt
"""
    },
    {
        "slug": "git-undo-revert",
        "title": "Undo: Revert",
        "student_task_summary": "Revert a commit.",
        "test_code": """
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-undo-revert", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    const out = readText(WS, "outputs/undo.txt").trim();
    assert.strictEqual(out, "HEAD=revert: bug: wrong value\\nVALUE=20\\nCOMMITS=4");
});
""",
        "solution_sh": """#!/bin/sh
set -e
mkdir -p outputs
rm -rf tmp/repo
mkdir -p tmp/repo && cd tmp/repo
git -c init.defaultBranch=main init -q
# Commits
echo "10" > calc.txt && git add calc.txt && git -c user.name="EF" -c user.email="ef@ex" commit -q -m "chore: base" --no-gpg-sign
echo "20" > calc.txt && git add calc.txt && git -c user.name="EF" -c user.email="ef@ex" commit -q -m "feat: increase" --no-gpg-sign
echo "999" > calc.txt && git add calc.txt && git -c user.name="EF" -c user.email="ef@ex" commit -q -m "bug: wrong value" --no-gpg-sign
# Revert
git revert --no-edit HEAD 
# Force message if needed (default is Revert "bug...")
# user spec requires exact "revert: bug: wrong value"
git commit --amend -m "revert: bug: wrong value" --no-edit --no-gpg-sign
# Report
HEAD=$(git log -1 --pretty=%s)
VALUE=$(cat calc.txt)
COMMITS=$(git rev-list --count HEAD)
echo "HEAD=$HEAD" > ../../outputs/undo.txt
echo "VALUE=$VALUE" >> ../../outputs/undo.txt
echo "COMMITS=$COMMITS" >> ../../outputs/undo.txt
"""
    },
    {
        "slug": "git-stash",
        "title": "Stash",
        "student_task_summary": "Stash and pop changes.",
        "test_code": """
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-stash", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    const out = readText(WS, "outputs/stash.txt").trim();
    assert.strictEqual(out, "STASHED=1\\nCLEAN_AFTER_STASH=1\\nRESTORED_WIP=work\\nRESTORED_TMP=scratch");
});
""",
        "solution_sh": """#!/bin/sh
set -e
mkdir -p outputs
rm -rf tmp/repo
mkdir -p tmp/repo && cd tmp/repo
git -c init.defaultBranch=main init -q
# Base
echo "base" > wip.txt
git add wip.txt
git -c user.name="EF" -c user.email="ef@ex" commit -q -m "chore: base" --no-gpg-sign
# Work
echo "work" > wip.txt
echo "scratch" > tmp.txt
# Stash
git stash push -u -q -m "wip: save"
# Check Clean
if [ -z "$(git status --porcelain)" ]; then CLEAN=1; else CLEAN=0; fi
# Pop
git stash pop -q
# Report
echo "STASHED=1" > ../../outputs/stash.txt
echo "CLEAN_AFTER_STASH=$CLEAN" >> ../../outputs/stash.txt
echo "RESTORED_WIP=$(cat wip.txt)" >> ../../outputs/stash.txt
echo "RESTORED_TMP=$(cat tmp.txt)" >> ../../outputs/stash.txt
"""
    },
    {
        "slug": "git-tags",
        "title": "Tags",
        "student_task_summary": "Create annotated tags.",
        "test_code": """
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-tags", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    const out = readText(WS, "outputs/tags.txt").trim();
    assert.strictEqual(out, "TAGS=v1.0.0\\nTAG_MESSAGE=Release 1.0.0\\nHEAD=feat: ship");
});
""",
        "solution_sh": """#!/bin/sh
set -e
mkdir -p outputs
rm -rf tmp/repo
mkdir -p tmp/repo && cd tmp/repo
git -c init.defaultBranch=main init -q
git -c user.name="EF" -c user.email="ef@ex" commit --allow-empty -q -m "chore: init" --no-gpg-sign
git -c user.name="EF" -c user.email="ef@ex" commit --allow-empty -q -m "feat: ship" --no-gpg-sign
# Tag
git tag -a v1.0.0 -m "Release 1.0.0"
# Report
TAGS=$(git tag)
MSG=$(git tag -n99 v1.0.0 | awk '{$1=""; print $0}' | sed 's/^ //')
HEAD=$(git log -1 --pretty=%s)

echo "TAGS=$TAGS" > ../../outputs/tags.txt
echo "TAG_MESSAGE=$MSG" >> ../../outputs/tags.txt
echo "HEAD=$HEAD" >> ../../outputs/tags.txt
"""
    },
    {
        "slug": "git-rebase-onto-main",
        "title": "Rebase",
        "student_task_summary": "Rebase feature branch onto main.",
        "test_code": """
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-rebase-onto-main", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    const out = readText(WS, "outputs/rebase.txt").trim();
    assert.strictEqual(out, "ORDER=chore: base|hotfix: patch|feat: one|feat: two\\nBRANCH=feature/x\\nBASE=main");
});
""",
        "solution_sh": """#!/bin/sh
set -e
mkdir -p outputs
rm -rf tmp/repo
mkdir -p tmp/repo && cd tmp/repo
git -c init.defaultBranch=main init -q
# Base
git -c user.name="EF" -c user.email="ef@ex" commit --allow-empty -q -m "chore: base" --no-gpg-sign
# Feature
git branch feature/x
git switch feature/x
git -c user.name="EF" -c user.email="ef@ex" commit --allow-empty -q -m "feat: one" --no-gpg-sign
git -c user.name="EF" -c user.email="ef@ex" commit --allow-empty -q -m "feat: two" --no-gpg-sign
# Hotfix on main
git switch main
git -c user.name="EF" -c user.email="ef@ex" commit --allow-empty -q -m "hotfix: patch" --no-gpg-sign
# Rebase
git switch feature/x
git rebase main
# Report
ORDER=$(git log --reverse --pretty=%s | tr '\\n' '|' | sed 's/|$//')
BRANCH=$(git branch --show-current)
BASE=$(git merge-base main feature/x) # Should be main's head? No, rebase moves it.
# Check if feature/x contains hotfix
BASE_NAME="unknown"
if git merge-base --is-ancestor main feature/x; then BASE_NAME="main"; fi
echo "ORDER=$ORDER" > ../../outputs/rebase.txt
echo "BRANCH=$BRANCH" >> ../../outputs/rebase.txt
echo "BASE=$BASE_NAME" >> ../../outputs/rebase.txt
"""
    }
]

import shutil

def main():
    root = Path.cwd()
    quests_dir = root / "data" / "quests"
    
    for q in QUESTS_SPECS:
        slug = q["slug"]
        print(f"Scaffolding {slug}...")
        q_dir = quests_dir / slug
        
        # Paths
        ws_dir = q_dir / "workspace"
        grading_dir = q_dir / "grading"
        
        # 1. Clean Directories (Workspace + Grading)
        # We want to keep q_dir but clean subdirs
        if ws_dir.exists(): shutil.rmtree(ws_dir)
        if grading_dir.exists(): shutil.rmtree(grading_dir)
        
        ws_dir.mkdir(parents=True, exist_ok=True)
        pub_dir = grading_dir / "public"
        sol_dir = grading_dir / "solutions"
        pub_dir.mkdir(parents=True, exist_ok=True)
        sol_dir.mkdir(parents=True, exist_ok=True)
        
        # 2. Write Files (Binary Mode for LF)
        
        # README
        readme_txt = f"# {q['title']}\n\n{q['student_task_summary']}\n"
        (ws_dir / "README.md").write_bytes(readme_txt.encode("utf-8"))
        
        # Starter task.sh
        starter_sh = "#!/bin/sh\n# TODO: Implement\necho 'TODO' > outputs/state.txt 2>/dev/null || true\nexit 0\n"
        (ws_dir / "task.sh").write_bytes(starter_sh.encode("utf-8"))
        
        # Tests
        test_txt = q["test_code"].replace("\r\n", "\n") # Ensure spec string is LF
        (pub_dir / f"{slug}.public.test.mjs").write_bytes(test_txt.encode("utf-8"))
        
        # Solution
        sol_txt = q["solution_sh"].replace("\r\n", "\n") # Ensure spec string is LF
        (sol_dir / "task.sh").write_bytes(sol_txt.encode("utf-8"))
    
    print("Done.")

if __name__ == "__main__":
    main()
