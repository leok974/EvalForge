# Briefing: Auto-Waiting

The CMS latency page simulates a system check: a content box appears after a 1 second delay. Your task: navigate to the page and assert the delayed element is visible.

Playwright's auto-waiting eliminates most explicit `sleep` calls. When you call `expect(locator).toBeVisible()`, Playwright retries the check until the element appears or the timeout is exceeded.
