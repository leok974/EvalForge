# Briefing: Custom Fixtures

Playwright fixtures let you define reusable test setup that is injected into tests automatically. A `loggedInPage` fixture handles authentication once and delivers a ready-to-use page to every test that needs it.

Your task: define a custom fixture using `test.extend`, then write two tests that use it to verify the dashboard.
