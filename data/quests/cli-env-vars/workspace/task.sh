#!/bin/sh
set -eu
mkdir -p outputs

mode="${MODE:-dev}"
port="${PORT:-3000}"

# Treat empty string as missing
[ -n "${mode}" ] || mode="dev"
[ -n "${port}" ] || port="3000"

printf "MODE=%s\nPORT=%s" "${mode}" "${port}" > outputs/config.txt
