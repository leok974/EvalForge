#!/bin/sh
set -e
mkdir -p outputs
rm -rf tmp/repo
mkdir -p tmp/repo && cd tmp/repo
git -c init.defaultBranch=main init -q
git -c user.name="EF" -c user.email="ef@ex" commit --allow-empty -q -m "chore: init" --no-gpg-sign
git -c user.name="EF" -c user.email="ef@ex" commit --allow-empty -q -m "feat: ship" --no-gpg-sign
# Tag
git tag -a v1.0.0 -m "Release 1.0.0"
# Report
TAGS=$(git tag)
MSG=$(git tag -n99 v1.0.0 | awk '{$1=""; print $0}' | sed 's/^ //')
HEAD=$(git log -1 --pretty=%s)

echo "TAGS=$TAGS" > ../../outputs/tags.txt
echo "TAG_MESSAGE=$MSG" >> ../../outputs/tags.txt
echo "HEAD=$HEAD" >> ../../outputs/tags.txt
