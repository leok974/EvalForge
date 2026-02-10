#!/bin/sh
set -eu
mkdir -p outputs

hosts="fixtures/hosts.txt"
reqs="fixtures/requests.txt"

# hosts.txt: "ip hostname"
resolve() {
  h="$1"
  ip="$(tr -d '\r' < "$hosts" | awk -v host="$h" '$2==host {print $1; exit}')"
  if [ -n "$ip" ]; then
    printf "%s %s\n" "$h" "$ip"
  else
    printf "%s NXDOMAIN\n" "$h"
  fi
}

: > outputs/resolved.txt
tr -d '\r' < "$reqs" | while IFS= read -r h; do
  [ -n "$h" ] || continue
  resolve "$h" >> outputs/resolved.txt
done
