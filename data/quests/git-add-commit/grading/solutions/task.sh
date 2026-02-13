#!/bin/sh
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
