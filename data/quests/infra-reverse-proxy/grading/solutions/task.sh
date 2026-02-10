#!/bin/sh
set -eu
mkdir -p outputs

conf="fixtures/nginx.conf"
: > outputs/routes.txt

# Very small parser:
# - capture location path from "location <path>"
# - capture proxy_pass url from "proxy_pass <url>;"
# - output mapping when both seen
# Robust parser using awk
# Handles both single-line and multi-line location/proxy_pass blocks
tr -d '\r' < "$conf" | awk '
  /location / {
    for(i=1;i<=NF;i++) if($i=="location") loc=$(i+1);
    gsub(/[{]/,"",loc);
  }
  /proxy_pass / {
    for(i=1;i<=NF;i++) if($i=="proxy_pass") url=$(i+1);
    gsub(/;$/,"",url);
    
    if(loc!="" && url!="") {
      print loc, "->", url;
      loc=""; # Reset for next mapping
    }
  }
' >> outputs/routes.txt
