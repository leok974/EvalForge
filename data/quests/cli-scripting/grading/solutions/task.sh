#!/bin/sh
set -eu

if [ "$#" -ne 2 ]; then
  echo "Usage: sh task.sh <src> <dst>" 1>&2
  exit 2
fi

src="$1"
dst="$2"

mkdir -p "$(dirname "$dst")"
cp "$src" "$dst"
