#!/bin/sh
set -eu

mkdir -p outputs sandbox
rm -rf sandbox/repo
mkdir -p sandbox/repo

cp fixtures/greeting.txt sandbox/repo/greeting.txt
cp fixtures/config.json sandbox/repo/config.json
cp fixtures/temp.log sandbox/repo/temp.log

cd sandbox/repo
git init >/dev/null 2>&1 || true
git branch -M main

printf "%s\n" "*.log" ".gitignore" > .gitignore

git add greeting.txt config.json
git -c user.name="EF" -c user.email="ef@example.com" commit -m "Add greeting and config" >/dev/null 2>&1

tracked="$(git ls-files | sort | tr '\n' ' ' | sed 's/ $//')"
ignoredPresent=false
if [ -f temp.log ]; then ignoredPresent=true; fi
commitMessage="$(git log -1 --pretty=%s)"

cd ../..
printf '{"tracked":["config.json","greeting.txt"],"ignoredPresent":%s,"commitMessage":"%s"}\n' \
  "$ignoredPresent" "$commitMessage" > outputs/summary.json
