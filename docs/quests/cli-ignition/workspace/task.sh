#!/bin/sh
set -eu

# 1) Current directory basename
CWD="$(basename "$(pwd)")"

# 2) Count regular files directly under fixtures/ (ignore subdirectories)
# -maxdepth 1 ensures "directly under"
# -type f ensures "regular files only"
FILES="$(find fixtures -maxdepth 1 -type f 2>/dev/null | wc -l | tr -d ' ')"

# 3) Print exactly 3 lines
echo "CWD=$CWD"
echo "FILES=$FILES"
echo "OK"
