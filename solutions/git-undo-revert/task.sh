#!/bin/sh
set -eu

mkdir -p outputs sandbox
rm -rf sandbox/repo
mkdir -p sandbox/repo

cd sandbox/repo
git init >/dev/null 2>&1 || true
git branch -M main

printf "good\n" > app.txt
git add app.txt
git -c user.name="EF" -c user.email="ef@example.com" commit -m "good" >/dev/null 2>&1

printf "bad\n" > app.txt
git add app.txt
git -c user.name="EF" -c user.email="ef@example.com" commit -m "bad" >/dev/null 2>&1

git revert --no-edit HEAD >/dev/null 2>&1

cd ../..
cp sandbox/repo/app.txt outputs/app.txt
git -C sandbox/repo log -3 --pretty=%s > outputs/log.txt
