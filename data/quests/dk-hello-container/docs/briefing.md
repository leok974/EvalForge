# Hello Container

A container is a lightweight, isolated environment that packages your application and its dependencies. Unlike a virtual machine, it shares the host OS kernel but keeps processes sandboxed.

A **Dockerfile** is the recipe for building a container image. Every image starts with a `FROM` instruction that names the base — the starting layer your image builds on top of.

## Your Task

Write a minimal Dockerfile that:

1. Starts `FROM` a base image (`alpine:3.18` is a tiny 5 MB Linux image — perfect for learning)
2. Adds a `CMD` instruction that prints `Hello from inside the container` when the container runs

The `CMD` instruction defines the default command. Use the **exec form** (a JSON array) rather than shell form:
- Exec form: `CMD ["echo", "Hello from inside the container"]`
- Shell form: `CMD echo Hello from inside the container`

Exec form is preferred because it doesn't invoke a shell process, which makes containers start faster and behave more predictably.
