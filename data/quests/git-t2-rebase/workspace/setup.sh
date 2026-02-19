#!/bin/sh
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
