## Outcome
You will learn how to package an app into a container image and run it as a service using Docker Compose.

## Concept in 30 seconds
A **Docker image** is a packaged filesystem + instructions. A **container** is a running instance of that image. A **Dockerfile** describes how to build an image. **Docker Compose** runs multiple containers together as “services” with networking, environment variables, and port mappings.

## Key terms
- **Image**: A packaged blueprint for a container.
- **Container**: A running instance of an image.
- **Dockerfile**: Build instructions for an image.
- **Docker Compose**: A tool to run multiple services together.
- **Port Mapping**: Exposing a container port to your host.

## Walkthrough
1) Write a Dockerfile that installs dependencies and runs your app.
2) Build the image and run it locally to confirm it starts.
3) Create a compose file to define the service: image/build, env vars, ports.
4) Use `docker compose up` to run it as a service.
5) Click **Run** to validate build/run commands; **Submit** when the service starts and behaves as required.

## Example implementation
A minimal Python web service container and compose file.

**Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "-m", "http.server", "8000"]
```

**docker-compose.yml**
```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=dev
```

Run it:
```bash
docker build -t demo-app .
docker run --rm -p 8000:8000 demo-app

# or with compose
docker compose up --build
```

## Common mistakes
- **Forgetting WORKDIR** and copying files into the wrong location.
- **Not exposing or mapping the correct port** (app runs but you can’t reach it).
- **Installing dependencies after copying source** (hurts cache efficiency); copy requirements first.
- **Binding to 127.0.0.1 inside the container** (use 0.0.0.0 for servers).
- **Confusing “image build” vs “container run”** (build creates image; run starts container).

## Check yourself
- What’s the difference between an image and a container?
- Why do we use a Dockerfile?
- What does port mapping do?
