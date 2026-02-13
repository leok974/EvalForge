#!/bin/sh
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
