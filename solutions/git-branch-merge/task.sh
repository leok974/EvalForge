#!/bin/sh
set -eu

mkdir -p outputs sandbox
rm -rf sandbox/repo
mkdir -p sandbox/repo

cd sandbox/repo
git init >/dev/null 2>&1 || true
git branch -M main

printf "base\n" > base.txt
git add base.txt
git -c user.name="EF" -c user.email="ef@example.com" commit -m "base" >/dev/null 2>&1

git checkout -b feature >/dev/null 2>&1
printf "feature\n" > feature.txt
git add feature.txt
git -c user.name="EF" -c user.email="ef@example.com" commit -m "feature work" >/dev/null 2>&1

git checkout main >/dev/null 2>&1
printf "main\n" > main.txt
git add main.txt
git -c user.name="EF" -c user.email="ef@example.com" commit -m "main work" >/dev/null 2>&1

git merge --no-ff feature -m "Merge feature" >/dev/null 2>&1

cd ../..
git -C sandbox/repo rev-list --parents -n 1 HEAD > outputs/parents.txt
