#!/bin/sh
set -e
sh ./setup.sh

# Attempt merge (will fail)
git merge feature || true

# Resolve conflict
echo "Resolved Content" > file.txt
git add file.txt
git commit -m "Merge branch 'feature'"
