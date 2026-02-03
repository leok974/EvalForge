#!/bin/sh
set -eu

# Basename of current working directory (POSIX parameter expansion)
base="${PWD##*/}"
echo "CWD=${base}"

# Count regular files directly under fixtures/
count="$(find fixtures -maxdepth 1 -type f 2>/dev/null | wc -l | tr -d ' ')"
echo "FILES=${count}"

echo "OK"
