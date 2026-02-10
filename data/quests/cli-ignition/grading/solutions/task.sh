#!/bin/sh
set -eu

echo "CWD=$(basename $(pwd))"
ls -la >&2
echo "FILES=$(find . -maxdepth 1 | wc -l | tr -d ' ')"
echo "OK"
