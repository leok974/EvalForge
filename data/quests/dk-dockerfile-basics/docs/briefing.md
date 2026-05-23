# Dockerfile Basics

You have a Python app (`app.py`) that prints a message. Your job is to containerise it with a proper Dockerfile.

A production-quality Dockerfile for a Python app typically has four instructions:

1. `FROM` — choose a base image
2. `WORKDIR` — set a working directory inside the container
3. `COPY` — copy source files from your machine into the image
4. `CMD` — specify the default command to run

## Your Task

Complete the Dockerfile so that:
- It uses `python:3.11-slim` as the base image
- It sets `/app` as the working directory
- It copies `app.py` into the container
- It runs `python app.py` using exec form

The `app.py` file is already provided — do not edit it.
