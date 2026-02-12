#!/bin/sh
set -eu

mkdir -p outputs sandbox
rm -rf sandbox/repo
mkdir -p sandbox/repo

cd sandbox/repo
git init >/dev/null 2>&1 || true
git branch -M main

printf "v1\n" > notes.txt
git add notes.txt
git -c user.name="EF" -c user.email="ef@example.com" commit -m "notes v1" >/dev/null 2>&1

printf "v2\n" > notes.txt
printf "tmp\n" > tmp.txt

git stash push -u -m "wip" >/dev/null 2>&1
git status --porcelain > ../../outputs/status_clean.txt
git stash list > ../../outputs/stash_list.txt

git stash apply >/dev/null 2>&1
git status --porcelain > ../../outputs/status_dirty.txt
