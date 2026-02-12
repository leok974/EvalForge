#!/bin/sh
set -eu

mkdir -p outputs sandbox
rm -rf sandbox/repo
mkdir -p sandbox/repo

cp fixtures/app_v1.txt sandbox/repo/app.txt

cd sandbox/repo
git init >/dev/null 2>&1 || true
git branch -M main

git add app.txt
git -c user.name="EF" -c user.email="ef@example.com" commit -m "init v1" >/dev/null 2>&1

cp ../../fixtures/app_v2.txt app.txt
cp ../../fixtures/notes.txt notes.md

cd ../..
git -C sandbox/repo status --porcelain > outputs/porcelain.txt
git -C sandbox/repo diff --stat > outputs/diffstat.txt
