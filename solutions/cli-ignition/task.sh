#!/bin/sh
set -eu

cwd="$(basename "$(pwd)")"

count=0
for f in fixtures/*; do
  [ -f "$f" ] && count=$((count + 1))
done

echo "CWD=$cwd"
echo "FILES=$count"
echo "OK"
