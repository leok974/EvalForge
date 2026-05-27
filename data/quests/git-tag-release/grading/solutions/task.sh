#!/bin/bash
set -eu
git init
git checkout -b main
echo "release content" > release.txt
git add release.txt
git commit -m "Initial commit"
git tag v1.0.0

mkdir -p outputs
git tag -l > outputs/tags.txt
