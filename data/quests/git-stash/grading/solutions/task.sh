#!/bin/sh
set -e
mkdir -p outputs
rm -rf tmp/repo
mkdir -p tmp/repo && cd tmp/repo
git -c init.defaultBranch=main init -q
# Base
echo "base" > wip.txt
git add wip.txt
git -c user.name="EF" -c user.email="ef@ex" commit -q -m "chore: base" --no-gpg-sign
# Work
echo "work" > wip.txt
echo "scratch" > tmp.txt
# Stash
git stash push -u -q -m "wip: save"
# Check Clean
if [ -z "$(git status --porcelain)" ]; then CLEAN=1; else CLEAN=0; fi
# Pop
git stash pop -q
# Report
echo "STASHED=1" > ../../outputs/stash.txt
echo "CLEAN_AFTER_STASH=$CLEAN" >> ../../outputs/stash.txt
echo "RESTORED_WIP=$(cat wip.txt)" >> ../../outputs/stash.txt
echo "RESTORED_TMP=$(cat tmp.txt)" >> ../../outputs/stash.txt
