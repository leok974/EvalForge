#!/bin/sh
set -eu
mkdir -p outputs

sym="$(tr -d '\r' < fixtures/diag.txt | awk -F= '$1=="SYMPTOM"{print $2; exit}')"

case "$sym" in
  502)
    printf "%s\n" \
      "Check reverse proxy upstream host/port" \
      "Verify backend /health from proxy network" \
      "Inspect backend logs for crash/restarts" \
      > outputs/next_steps.txt
    ;;
  401)
    printf "%s\n" \
      "Confirm auth headers/cookies are present" \
      "Verify cookie domain/SameSite/Secure alignment" \
      "Check auth middleware logs for rejects" \
      > outputs/next_steps.txt
    ;;
  CORS)
    printf "%s\n" \
      "Verify Access-Control-Allow-Origin matches request origin" \
      "Confirm Access-Control-Allow-Credentials when using cookies" \
      "Check preflight OPTIONS handling and allowed headers" \
      > outputs/next_steps.txt
    ;;
  *)
    printf "%s\n" \
      "Check health endpoint and status codes" \
      "Inspect recent logs for the first error" \
      "Validate config/env and recent deploy changes" \
      > outputs/next_steps.txt
    ;;
esac
