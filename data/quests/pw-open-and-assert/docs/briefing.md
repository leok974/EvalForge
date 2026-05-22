# Briefing: Open and Assert

Your first mission: navigate to the CMS login page and verify the page title.

Playwright's `page.goto()` command navigates to any URL. Combined with `expect(page).toHaveTitle()`, you can assert exactly what page you've landed on — a critical first step in any automation script.

The CMS is running at your configured `baseURL`. Navigate to the root path `'/'` and confirm the title reads "CMS Login".
