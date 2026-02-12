#!/bin/sh
set -eu

mkdir -p outputs

MODE="${MODE:-dev}"
PORT="${PORT:-3000}"

printf "MODE=%s\nPORT=%s\n" "$MODE" "$PORT" > outputs/config.txt
