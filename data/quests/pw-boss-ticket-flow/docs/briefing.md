# Boss Quest: Dispute Resolution Flow

This is the capstone challenge for the Playwright Systems track. You will implement a complete automated test suite covering the full CMS dispute resolution workflow.

Your suite must:
1. Log in to the CMS in a `beforeEach` hook
2. Navigate to `/disputes` and verify the disputes table
3. Navigate into a dispute detail page via the view link
4. Assert the dispute detail panel is visible
5. Click the resolve button and assert the success state appears
6. Capture a screenshot as evidence

All test cases must pass with a structured `test.describe` block.
