#!/bin/sh
set -eu
mkdir -p outputs

log="fixtures/app.log"

info="$(grep -c "^INFO " "$log" 2>/dev/null || true)"
warn="$(grep -c "^WARN " "$log" 2>/dev/null || true)"
err="$(grep -c "^ERROR " "$log" 2>/dev/null || true)"

# Most common error token is second word after "ERROR"
top="$(
  grep "^ERROR " "$log" 2>/dev/null \
    | awk '{print $2}' \
    | sort \
    | uniq -c \
    | awk '{print $2 " " $1}' \
    | sort -k2,2nr -k1,1 \
    | head -n 1 \
    | awk '{print $1}'
)"
[ -n "$top" ] || top=""

printf "app_log_info_total %s\napp_log_warnings_total %s\napp_log_errors_total %s\n" "$info" "$warn" "$err" > outputs/metrics.prom
printf "%s\n" "$top" > outputs/top_error.txt
