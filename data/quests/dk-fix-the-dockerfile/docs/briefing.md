# Fix the Dockerfile

This Dockerfile has **three bugs**. Your job is to find and fix all of them.

The app it builds (`app.py`) just prints `"Fixed!"` — so the Dockerfile is the only thing that needs attention.

## Rules

- Read the Dockerfile carefully
- Fix all three bugs
- Do not change `app.py`

## Hints on what to look for

Docker instructions are case-sensitive keywords (`FROM`, `WORKDIR`, `COPY`, `CMD`, etc.). Typos in instruction names or image names will prevent the build from working. And remember: `CMD` has a preferred form.
