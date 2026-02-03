# Reverse Proxy

Fix `nginx.conf` so it routes:

* `/api/*` → `http://api:8000/*` **with prefix stripped**
* `/` → `http://web:5173/`

We enforce the safe nginx pattern:

* `location /api/ { proxy_pass http://api:8000/; }` (note the trailing `/`)
