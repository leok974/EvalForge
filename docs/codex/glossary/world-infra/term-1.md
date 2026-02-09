---
title: Reverse Proxy
id: glossary/world-infra/term-1
world: world-infra
level: intermediate
tags: [networking, routing, nginx]
related:
  - codex:glossary/infra/container
  - codex:glossary/infra/port-mapping
---

# Reverse Proxy

## Definition
A reverse proxy sits in front of services and routes incoming requests to the right backend (e.g., Nginx routing `/api` to the API container). It centralizes TLS, routing, headers, and compression.

## Usage
- Route multiple apps by hostname/path.
- Terminate TLS.
- Set security headers and cache rules.

## Example
```nginx
location /api/ {
  proxy_pass http://api:8000/;
  proxy_set_header Host $host;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

## Pitfalls

* Missing trailing slashes in `proxy_pass` can break paths.
* Not forwarding headers can break auth/cookies.

## Related

* Container: reverse proxies route traffic to containers.
* Port Mapping: proxies use port mapping to reach services.