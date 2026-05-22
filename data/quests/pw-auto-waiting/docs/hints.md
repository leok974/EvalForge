# Hints

## Hint 1
The delayed element has `data-testid="delayed-protocol-box"`. Navigate to `/latency?delay=1`.

## Hint 2
Remove the `{ timeout: 100 }` override from the assertion — the default 30s timeout is enough for a 1s delay.

## Hint 3
Your solution is simply: `await expect(page.getByTestId('delayed-protocol-box')).toBeVisible();`
