# Briefing: Screenshot and Trace

Visual evidence is a cornerstone of automation. Your task: navigate to the CMS login page, capture a screenshot, and verify the file was written to disk.

Playwright's `page.screenshot()` captures the full page or a specific element. Combined with Node's `fs.existsSync`, you can confirm the artifact was created.
