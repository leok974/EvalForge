# Docker Compose

## Definition
**Docker Compose** runs multiple containers together as named services. It defines networking, environment variables, ports, volumes, and dependencies in a `docker-compose.yml`.

## Tiny example
`docker compose up --build` builds images and starts services defined in the compose file.

## Common pitfall
If your service “runs” but can’t be reached, the problem is often ports or binding:
- map ports in compose
- ensure your app binds to `0.0.0.0` inside the container

## Related
Container, Port Mapping
