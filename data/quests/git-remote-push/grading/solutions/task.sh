#!/bin/bash
set -eu
git init
git checkout -b main
echo "content" > file.txt
git add file.txt
git commit -m "Initial commit"

# Create bare local remote
mkdir -p remote.git
git init --bare remote.git

git remote add origin ./remote.git
git push -u origin main

mkdir -p outputs
ls remote.git/refs/heads/ > outputs/refs.txt
