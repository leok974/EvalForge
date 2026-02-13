#!/bin/sh
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
