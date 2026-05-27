# Briefing: Browser Configuration

Playwright supports chromium, firefox, and webkit. You can override the browser per test file using `test.use({ browserName: 'chromium' })`. This is the foundation for cross-browser test strategies.

Your task: explicitly configure your test to run in chromium, then verify the CMS login page loads and assert the browser name.
