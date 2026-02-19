#!/bin/bash
set -eu
git init
git checkout -b main
echo "root" > root.txt
git add root.txt
git commit -m "Root commit"

git checkout -b feature
echo "feat" > feat.txt
git add feat.txt
git commit -m "Feature commit"

git checkout main
echo "main update" >> root.txt
git add root.txt
git commit -m "Main update"

git checkout feature
git rebase main

git checkout main
git merge feature --ff-only

mkdir -p outputs
git log --oneline > outputs/log.txt
