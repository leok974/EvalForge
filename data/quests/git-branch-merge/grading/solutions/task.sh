#!/bin/bash
set -eu
git init
git checkout -b main
echo "main content" > main.txt
git add main.txt
git commit -m "Initial commit on main"

git checkout -b feature
echo "feature content" > feature.txt
git add feature.txt
git commit -m "Add feature"

git checkout main
git merge feature --no-ff -m "Merge feature into main"

mkdir -p outputs
git log --pretty=format:"%P" -1 HEAD > outputs/parents.txt
