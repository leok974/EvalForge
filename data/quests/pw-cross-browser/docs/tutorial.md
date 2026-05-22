# Tutorial: Browser Configuration

## test.use()

`test.use()` overrides configuration for all tests in the current file or describe block:

```typescript
// Run this file's tests in chromium
test.use({ browserName: 'chromium' });

// Run with specific viewport
test.use({ viewport: { width: 1280, height: 720 } });

// Run with geolocation
test.use({ geolocation: { latitude: 51.5, longitude: -0.1 }, permissions: ['geolocation'] });
```

## Cross-Browser in playwright.config.ts

The canonical cross-browser setup uses projects in the config file:

```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'firefox',  use: { browserName: 'firefox'  } },
    { name: 'webkit',   use: { browserName: 'webkit'   } },
  ],
});
```

When you run `npx playwright test`, all three projects execute.

## Accessing Browser Info at Runtime

```typescript
const browserName = page.context().browser()?.browserType().name();
// 'chromium' | 'firefox' | 'webkit'
```

## Available Browsers

Playwright supports:
- `chromium` (Chrome/Edge engine)
- `firefox`
- `webkit` (Safari engine)

Install them with: `npx playwright install`
