#!/bin/sh
set -eu

mkdir -p outputs sandbox
rm -rf sandbox/repo sandbox/remote.git
mkdir -p sandbox/repo

cd sandbox/repo
git init >/dev/null 2>&1 || true
git branch -M main

printf "init\n" > file.txt
git add file.txt
git -c user.name="EF" -c user.email="ef@example.com" commit -m "init" >/dev/null 2>&1

cd ..
git init --bare remote.git >/dev/null 2>&1

cd repo
git remote add origin ../remote.git
git push -u origin main >/dev/null 2>&1

cd ../..
git --git-dir=sandbox/remote.git show-ref > outputs/refs.txt
