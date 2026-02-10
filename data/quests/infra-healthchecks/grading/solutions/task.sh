#!/bin/sh
set -eu
mkdir -p outputs

# Parse: name code latency
ok=0
total=0
failed=""
slow_name=""
slow_ms=-1

while IFS= read -r line; do
  line="$(printf "%s" "$line" | tr -d '\r')"
  [ -n "$line" ] || continue
  name="$(printf "%s" "$line" | awk '{print $1}')"
  code="$(printf "%s" "$line" | awk '{print $2}')"
  ms="$(printf "%s" "$line" | awk '{print $3}')"

  total=$((total+1))
  if [ "$code" -eq 200 ] 2>/dev/null; then
    ok=$((ok+1))
  else
    if [ -z "$failed" ]; then failed="$name"; else failed="$failed,$name"; fi
  fi

  if [ "$ms" -gt "$slow_ms" ] 2>/dev/null; then
    slow_ms="$ms"
    slow_name="$name"
  fi
done < fixtures/health.txt

score=$((ok * 100 / total))

status="OK"
[ -z "$failed" ] || status="DEGRADED"

printf "STATUS=%s\nFAILED=%s\nSLOWEST=%s %s\n" "$status" "$failed" "$slow_name" "$slow_ms" > outputs/health_status.txt
printf "%s\n" "$score" > outputs/health_score.txt
