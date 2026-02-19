#!/bin/sh
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
