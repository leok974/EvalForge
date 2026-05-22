# Briefing: API Testing

Playwright's `request` fixture provides a context for making direct HTTP requests — no browser required. Your task: use `request.get()` to call the CMS health endpoint `/healthz` and assert both the status code and the JSON body.
