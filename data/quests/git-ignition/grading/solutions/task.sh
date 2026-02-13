#!/bin/sh
set -e
mkdir -p outputs
rm -rf tmp/repo
mkdir -p tmp/repo
cd tmp/repo
git -c init.defaultBranch=main init -q
echo "Hello, EvalForge!" > hello.txt
git add hello.txt
git -c user.name="EvalForge" -c user.email="evalforge@example.com" commit -q -m "chore: initial commit" --no-gpg-sign

# Generat output
echo "BRANCH=$(git branch --show-current)" > ../../outputs/state.txt
echo "COMMITS=$(git rev-list --count HEAD)" >> ../../outputs/state.txt
echo "FILES=$(ls)" >> ../../outputs/state.txt
