#!/usr/bin/env bash
set -euo pipefail
TAG="generic"; CMD=""; ART=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --tag) TAG="$2"; shift 2;;
    --cmd) CMD="$2"; shift 2;;
    --art) ART="$2"; shift 2;;
    *) echo "Unknown arg $1"; exit 2;;
  esac
done
[ -n "$CMD" ] || { echo "Missing --cmd"; exit 2; }

LOG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)/logs"
mkdir -p "$LOG_DIR"

STDOUT_FILE="$(mktemp)"; STDERR_FILE="$(mktemp)"
# shellcheck disable=SC2086
bash -lc "$CMD" >"$STDOUT_FILE" 2>"$STDERR_FILE"; EC=$?

STDOUT_TAIL="$(tail -n 50 "$STDOUT_FILE" || true)"
STDERR_TAIL="$(tail -n 50 "$STDERR_FILE" || true)"

FINGERPRINT=""
if [ $EC -ne 0 ]; then
  FINGERPRINT="$(printf "%s" "$STDERR_TAIL" | sha1sum | awk '{print $1}')"
fi

ART_JSON="null"
if [ -n "$ART" ] && [ -f "$ART" ]; then
  ART_JSON="$(cat "$ART")"
fi

TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
CWD="$(pwd)"
QUEST_ID="${QUEST_ID:-null}"

# Append NDJSON
JOURNAL="$LOG_DIR/error-journal.ndjson"
printf '{"ts":"%s","os":"%s","tag":"%s","cwd":"%s","command":"%s","exit_code":%d,"fingerprint":"%s","stdout_tail":%s,"stderr_tail":%s,"artifact":%s,"quest_id":%s}\n' \
  "$TS" "unix" "$TAG" "$CWD" "$CMD" "$EC" "$FINGERPRINT" \
  "$(jq -Rn --arg s "$STDOUT_TAIL" '$s')" \
  "$(jq -Rn --arg s "$STDERR_TAIL" '$s')" \
  "$ART_JSON" \
  "$(jq -n --arg q "$QUEST_ID" 'if $q == "" or $q == "null" then null else $q end')" \
  >> "$JOURNAL"

# Stream real output
cat "$STDOUT_FILE"; cat "$STDERR_FILE" >&2
exit $EC
