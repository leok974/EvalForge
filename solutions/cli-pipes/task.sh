#!/bin/sh
set -eu

mkdir -p outputs

# top 2 most frequent names as: "name count"
sort fixtures/names.txt \
  | uniq -c \
  | sort -nr \
  | head -n 2 \
  | awk '{print $2" "$1}' \
  > outputs/top.txt
