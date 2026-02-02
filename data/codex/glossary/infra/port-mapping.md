# Port Mapping

## Definition
**Port mapping** exposes a container port to your host machine using the format `host_port:container_port`. This is how you access a service running inside a container from your browser or other host processes.

## Tiny example
`- "8000:8000"` means: host port 8000 forwards to container port 8000.

## Common pitfall
If the app binds to `127.0.0.1` inside the container, port mapping won’t help. Servers inside containers should bind to `0.0.0.0` so they listen on all interfaces.

## Related
Docker Compose, Container
