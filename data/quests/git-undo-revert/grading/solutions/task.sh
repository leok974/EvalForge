#!/bin/sh
set -e
mkdir -p outputs
rm -rf tmp/repo
mkdir -p tmp/repo && cd tmp/repo
git -c init.defaultBranch=main init -q
# Commits
echo "10" > calc.txt && git add calc.txt && git -c user.name="EF" -c user.email="ef@ex" commit -q -m "chore: base" --no-gpg-sign
echo "20" > calc.txt && git add calc.txt && git -c user.name="EF" -c user.email="ef@ex" commit -q -m "feat: increase" --no-gpg-sign
echo "999" > calc.txt && git add calc.txt && git -c user.name="EF" -c user.email="ef@ex" commit -q -m "bug: wrong value" --no-gpg-sign
# Revert
git revert --no-edit HEAD 
# Force message if needed (default is Revert "bug...")
# user spec requires exact "revert: bug: wrong value"
git commit --amend -m "revert: bug: wrong value" --no-edit --no-gpg-sign
# Report
HEAD=$(git log -1 --pretty=%s)
VALUE=$(cat calc.txt)
COMMITS=$(git rev-list --count HEAD)
echo "HEAD=$HEAD" > ../../outputs/undo.txt
echo "VALUE=$VALUE" >> ../../outputs/undo.txt
echo "COMMITS=$COMMITS" >> ../../outputs/undo.txt
