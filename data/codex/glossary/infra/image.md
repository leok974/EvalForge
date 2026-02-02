# Image

## Definition
A **Docker image** is a packaged blueprint that contains a filesystem and instructions for running an application. Images are built from a Dockerfile and can be reused to run many containers.

## Tiny example
`docker build -t demo-app .` builds an image named `demo-app`.

## Common pitfall
An image is not “running.” If your app isn’t accessible, make sure you started a container (`docker run`) and mapped ports correctly.

## Related
Container, Dockerfile
