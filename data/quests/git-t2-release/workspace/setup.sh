#!/bin/sh
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
