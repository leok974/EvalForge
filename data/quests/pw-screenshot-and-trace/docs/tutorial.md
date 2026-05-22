# Tutorial: Screenshots

## page.screenshot()

Captures a PNG of the current viewport:

```typescript
import * as fs from 'fs';

// Full-page screenshot saved to a path:
await page.screenshot({ path: '/tmp/screenshot.png' });

// Full-page (scrolled):
await page.screenshot({ path: '/tmp/full.png', fullPage: true });

// As a buffer (no file write):
const buffer = await page.screenshot();

// Element screenshot:
const element = page.getByTestId('dashboard-title');
await element.screenshot({ path: '/tmp/element.png' });
```

## Verifying the File

Use Node's `fs` module to confirm the file was written:

```typescript
import * as fs from 'fs';
expect(fs.existsSync('/tmp/screenshot.png')).toBe(true);
```

## Trace Viewer

Playwright's trace viewer records a full execution trace (screenshots, network, DOM snapshots):

```typescript
// In playwright.config.ts:
use: { trace: 'on-first-retry' }

// Or programmatically:
await context.tracing.start({ screenshots: true, snapshots: true });
// ... your test ...
await context.tracing.stop({ path: '/tmp/trace.zip' });
```

Run `npx playwright show-trace trace.zip` to open the viewer.
