#!/bin/sh
set -eu

# Helper to get Windows-friendly path if available (Git Bash), else standard pwd
get_pwd() {
  pwd -W 2>/dev/null || pwd
}

root="$(get_pwd)"
mkdir -p outputs

cd fixtures/site/pages
get_pwd > "$root/outputs/location.txt"
ls -1 > "$root/outputs/pages.txt"

cd "$root"
get_pwd > outputs/back.txt
