#!/bin/sh
set -eu
mkdir -p outputs

file="fixtures/app.env"

get_kv() {
  key="$1"
  # last occurrence wins; strip CR
  tr -d '\r' < "$file" | awk -F= -v k="$key" '$1==k {v=$2} END{print v}'
}

mode="${MODE:-}"
port="${PORT:-}"
log="${LOG_LEVEL:-}"

[ -n "$mode" ] || mode="$(get_kv MODE)"
[ -n "$port" ] || port="$(get_kv PORT)"
[ -n "$log" ]  || log="$(get_kv LOG_LEVEL)"

[ -n "$mode" ] || mode="dev"
[ -n "$port" ] || port="3000"
[ -n "$log" ]  || log="info"

# validate port: integer 1..65535
case "$port" in
  ''|*[!0-9]*)
    echo "EF_INFRA_ENV_PORT_INVALID" 1>&2
    exit 12
    ;;
esac
if [ "$port" -lt 1 ] || [ "$port" -gt 65535 ]; then
  echo "EF_INFRA_ENV_PORT_INVALID" 1>&2
  exit 12
fi

printf "MODE=%s\nPORT=%s\nLOG_LEVEL=%s\n" "$mode" "$port" "$log" > outputs/runtime.env
