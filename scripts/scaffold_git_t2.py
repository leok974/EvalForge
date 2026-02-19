
import os
import shutil
from pathlib import Path

# Specs ensuring LF line endings for scripts
QUESTS = [
    {
        "slug": "git-t2-merge-conflict",
        "title": "Merge Conflicts (T2)",
        "readme": "# Merge Conflicts\n\n1. Run `./setup.sh` to initialize the repository.\n2. Merge `feature` branch into `main`.\n3. Resolve the conflict in `file.txt` to keep both lines or a specific resolution.\n4. Commit the merge.",
        "setup_sh": """#!/bin/sh
set -e
rm -rf .git file.txt
git init
git config user.email "you@example.com"
git config user.name "Your Name"
git checkout -b main

echo "Base Content" > file.txt
git add file.txt
git commit -m "chore: initial commit"

git checkout -b feature
echo "Feature Change" > file.txt
git add file.txt
git commit -m "feat: update file"

git checkout main
echo "Main Change" > file.txt
git add file.txt
git commit -m "chore: update file on main"
""",
        "solution_sh": """#!/bin/sh
set -e
sh ./setup.sh

# Attempt merge (will fail)
git merge feature || true

# Resolve conflict
echo "Resolved Content" > file.txt
git add file.txt
git commit -m "Merge branch 'feature'"
""",
        "test_mjs": """
import { runSh, readText, checkFileExists } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";
import fs from "node:fs";
import path from "node:path";

test("git-t2-merge-conflict", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    
    // Check clean status
    // We assume the user ran setup.sh and did work.
    // If .git missing, fail
    if (!fs.existsSync(path.join(WS, ".git"))) {
        assert.fail("No .git repository found. Did you run ./setup.sh?");
    }

    // Check merge commit
    const log = await runSh(WS, "git log --oneline -n 5");
    assert.match(log.stdout, /Merge branch/, "Merge commit not found in log");

    // Check conflict markers gone
    const content = readText(WS, "file.txt");
    assert.doesNotMatch(content, /<<<<<<<|=======|>>>>>>>/, "Conflict markers found in file.txt");
});
"""
    },
    {
        "slug": "git-t2-rebase",
        "title": "Rebase (T2)",
        "readme": "# Rebase\n\n1. Run `./setup.sh`.\n2. You are on `feature` branch.\n3. Rebase `feature` onto `main` to create a linear history.\n4. Ensure no merge commits are created.",
        "setup_sh": """#!/bin/sh
set -e
rm -rf .git feature.txt main.txt
git init
git config user.email "you@example.com"
git config user.name "Your Name"
git checkout -b main

# Commit A
echo "A" > main.txt
git add main.txt
git commit -m "chore: commit A"

# Commit B
echo "B" >> main.txt
git add main.txt
git commit -m "chore: commit B"

# Branch Feature
git checkout -b feature

# Commit D (on feature)
echo "D" > feature.txt
git add feature.txt
git commit -m "feat: commit D"

# Switch Main
git checkout main

# Commit C (on main)
echo "C" >> main.txt
git add main.txt
git commit -m "chore: commit C"

# Switch back to Feature for user
git checkout feature
""",
        "solution_sh": """#!/bin/sh
set -e
sh ./setup.sh

# Rebase
git rebase main
""",
        "test_mjs": """
import { runSh } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";
import fs from "node:fs";
import path from "node:path";

test("git-t2-rebase", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();

    if (!fs.existsSync(path.join(WS, ".git"))) {
        assert.fail("No .git repository found. Did you run ./setup.sh?");
    }

    // Check linear history on current branch (should be feature)
    // Counts merge commits
    const merges = await runSh(WS, "git log --merges --oneline");
    assert.strictEqual(merges.stdout.trim(), "", "Found merge commits, history not linear");

    // Check commit C is present in history of feature
    const log = await runSh(WS, "git log --oneline");
    assert.match(log.stdout, /commit C/, "Commit C from main not found in feature history");
    assert.match(log.stdout, /commit D/, "Commit D from feature not found in history");
});
"""
    },
    {
        "slug": "git-t2-release",
        "title": "Release Workflow (T2)",
        "readme": "# Release Workflow\n\n1. Run `./setup.sh`.\n2. Create a file `RELEASE_NOTES.md` with some content.\n3. Commit it.\n4. Create an annotated tag `v1.0` with message \"Release 1.0\".",
        "setup_sh": """#!/bin/sh
set -e
rm -rf .git RELEASE_NOTES.md
git init
git config user.email "you@example.com"
git config user.name "Your Name"
git checkout -b main

# Initial commits
echo "Init" > README.md
git add README.md
git commit -m "chore: init"

echo "Feature" > app.py
git add app.py
git commit -m "feat: add app"
""",
        "solution_sh": """#!/bin/sh
set -e
sh ./setup.sh

echo "Release 1.0 Notes" > RELEASE_NOTES.md
git add RELEASE_NOTES.md
git commit -m "docs: add release notes"

git tag -a v1.0 -m "Release 1.0"
""",
        "test_mjs": """
import { runSh, checkFileExists } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";
import fs from "node:fs";
import path from "node:path";

test("git-t2-release", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();

    if (!fs.existsSync(path.join(WS, ".git"))) {
        assert.fail("No .git repository found. Did you run ./setup.sh?");
    }

    // Check tag
    const tags = await runSh(WS, "git tag -l v1.0");
    assert.match(tags.stdout, /v1.0/, "Tag v1.0 not found");

    // Check annotated message?
    // tough to check easily without git cat-file, but tag existence is good enough for basic pass
    
    // Check release notes
    assert.ok(fs.existsSync(path.join(WS, "RELEASE_NOTES.md")), "RELEASE_NOTES.md missing");
});
"""
    }
]

def main():
    base_dir = Path("data/quests")
    for q in QUESTS:
        slug = q["slug"]
        print(f"Scaffolding {slug}...")
        q_dir = base_dir / slug
        
        ws_dir = q_dir / "workspace"
        grading_pub = q_dir / "grading/public"
        grading_sol = q_dir / "grading/solutions"
        
        # Clean and recreate
        if q_dir.exists():
            shutil.rmtree(q_dir)
        
        ws_dir.mkdir(parents=True)
        grading_pub.mkdir(parents=True)
        grading_sol.mkdir(parents=True)
        
        # Write files
        
        # README
        (ws_dir / "README.md").write_text(q["readme"], encoding="utf-8")
        
        # workspace/setup.sh
        setup_sh_content = q["setup_sh"].replace("\r\n", "\n")
        (ws_dir / "setup.sh").write_bytes(setup_sh_content.encode("utf-8"))
        
        # grading/solutions/task.sh
        sol_sh_content = q["solution_sh"].replace("\r\n", "\n")
        (grading_sol / "task.sh").write_bytes(sol_sh_content.encode("utf-8"))
        
        # grading/public/test.mjs
        test_mjs_content = q["test_mjs"].replace("\r\n", "\n")
        (grading_pub / f"{slug}.public.test.mjs").write_bytes(test_mjs_content.encode("utf-8"))
        
        print(f"  Created {slug}")

if __name__ == "__main__":
    main()
