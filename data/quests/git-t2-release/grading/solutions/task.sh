#!/bin/sh
set -e
sh ./setup.sh

echo "Release 1.0 Notes" > RELEASE_NOTES.md
git add RELEASE_NOTES.md
git commit -m "docs: add release notes"

git tag -a v1.0 -m "Release 1.0"
