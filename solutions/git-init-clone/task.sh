#!/bin/sh
set -eu

mkdir -p outputs sandbox
rm -rf sandbox/repo sandbox/remote.git sandbox/clone
mkdir -p sandbox/repo

cp fixtures/hello.txt sandbox/repo/hello.txt

cd sandbox/repo
git init >/dev/null 2>&1 || true
git branch -M main

git add hello.txt
git -c user.name="EF" -c user.email="ef@example.com" commit -m "init" >/dev/null 2>&1

cd ..
git clone --bare repo remote.git >/dev/null 2>&1
git clone remote.git clone >/dev/null 2>&1

cd ..
commitCount="$(git -C sandbox/repo rev-list --count HEAD)"
headMessage="$(git -C sandbox/repo log -1 --pretty=%s)"
branch="$(git -C sandbox/repo branch --show-current)"

if [ -d sandbox/clone/.git ]; then cloneHasGit=true; else cloneHasGit=false; fi

printf '{"repoExists":true,"branch":"%s","commitCount":%s,"headMessage":"%s","cloneHasGit":%s}\n' \
  "$branch" "$commitCount" "$headMessage" "$cloneHasGit" > outputs/report.json
