#!/bin/sh
set -eu
mkdir -p outputs

origin="$(tr -d '\r' < fixtures/request_origin.txt | sed -n '1p')"
headers="$(tr -d '\r' < fixtures/response_headers.txt)"

acao="$(printf "%s\n" "$headers" | awk -F': ' 'tolower($1)=="access-control-allow-origin" {print $2; exit}')"
acc="$(printf "%s\n" "$headers" | awk -F': ' 'tolower($1)=="access-control-allow-credentials" {print $2; exit}')"
cookie="$(printf "%s\n" "$headers" | awk -F': ' 'tolower($1)=="set-cookie" {print $2; exit}')"

cors_ok="false"
if [ "$acao" = "*" ] || [ "$acao" = "$origin" ]; then cors_ok="true"; fi

cred="false"
[ "$acc" = "true" ] && cred="true"

cookie_secure="false"
printf "%s" "$cookie" | grep -qi "Secure" && cookie_secure="true"

samesite="$(printf "%s" "$cookie" | sed -n 's/.*SameSite=\([^;]*\).*/\1/p' | head -n 1)"
[ -n "$samesite" ] || samesite="Unknown"

printf "CORS_OK=%s\nCREDENTIALS=%s\nCOOKIE_SECURE=%s\nCOOKIE_SAMESITE=%s\n" \
  "$cors_ok" "$cred" "$cookie_secure" "$samesite" > outputs/security_report.txt
