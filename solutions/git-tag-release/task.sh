#!/bin/sh
set -eu

mkdir -p outputs sandbox
rm -rf sandbox/repo
mkdir -p sandbox/repo

cd sandbox/repo
git init >/dev/null 2>&1 || true
git branch -M main

printf "v1\n" > file.txt
git add file.txt
git -c user.name="EF" -c user.email="ef@example.com" commit -m "init" >/dev/null 2>&1

git -c user.name="EF" -c user.email="ef@example.com" tag -a v1.0.0 -m "Release v1.0.0"

git cat-file -t v1.0.0 > ../../outputs/tag_type.txt
git rev-parse 'v1.0.0^{}' > ../../outputs/tag_target.txt
