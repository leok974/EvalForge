# Container

## Definition
A **container** is a running instance of an image. It has its own process space and filesystem view, but shares the host kernel. Containers are meant to be disposable and reproducible.

## Tiny example
`docker run --rm demo-app` starts a container from the `demo-app` image, runs it, then removes it afterward.

## Common pitfall
Changes made inside a container are usually ephemeral unless you use volumes. Don’t “store important data” inside containers unless you’ve mounted persistent storage.

## Related
Image, Docker Compose
