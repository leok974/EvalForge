#!/bin/sh
set -eu
mkdir -p outputs

# Expect header line: Proto LocalAddress PID Program
# Data line: tcp 0.0.0.0:8000 222 uvicorn
# Extract addr/port and program (col2 and col4)

tr -d '\r' < fixtures/netstat.txt | tail -n +2 \
  | awk '
    {
      split($2, a, ":");
      host=a[1]; port=a[2]; prog=$4;
      if (host=="0.0.0.0") print port, prog > "outputs/public_ports.tmp";
      else if (host=="127.0.0.1") print port, prog > "outputs/localhost_ports.tmp";
    }
  '

# Sort by numeric port
( [ -f outputs/public_ports.tmp ] && sort -n -k1,1 outputs/public_ports.tmp || true ) > outputs/public_ports.txt
( [ -f outputs/localhost_ports.tmp ] && sort -n -k1,1 outputs/localhost_ports.tmp || true ) > outputs/localhost_ports.txt
rm -f outputs/public_ports.tmp outputs/localhost_ports.tmp
