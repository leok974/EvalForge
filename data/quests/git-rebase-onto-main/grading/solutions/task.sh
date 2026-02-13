#!/bin/sh
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
ORDER=$(git log --reverse --pretty=%s | tr '\n' '|' | sed 's/|$//')
BRANCH=$(git branch --show-current)
BASE=$(git merge-base main feature/x) # Should be main's head? No, rebase moves it.
# Check if feature/x contains hotfix
BASE_NAME="unknown"
if git merge-base --is-ancestor main feature/x; then BASE_NAME="main"; fi
echo "ORDER=$ORDER" > ../../outputs/rebase.txt
echo "BRANCH=$BRANCH" >> ../../outputs/rebase.txt
echo "BASE=$BASE_NAME" >> ../../outputs/rebase.txt
