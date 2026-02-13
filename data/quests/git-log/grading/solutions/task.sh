#!/bin/sh
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
