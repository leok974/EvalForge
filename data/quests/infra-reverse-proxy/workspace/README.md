# Infra Reverse Proxy: Nginx Route Extractor

Parse fixtures/nginx.conf to find route mappings.
Extract paths from `location <path>` and targets from `proxy_pass <target>`.
Write routes to outputs/routes.txt as:
`<path> -> <target>`

Preserve file order.
