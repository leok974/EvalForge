#!/bin/sh
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
