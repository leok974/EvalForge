# Hints

## Hint 1
`page.screenshot({ path: '/tmp/cms-login.png' })` saves a PNG to that path.

## Hint 2
After taking the screenshot, use `fs.existsSync('/tmp/cms-login.png')` to check the file was created. Import `fs` at the top: `import * as fs from 'fs';`

## Hint 3
```typescript
const screenshotPath = '/tmp/cms-login.png';
await page.screenshot({ path: screenshotPath });
expect(fs.existsSync(screenshotPath)).toBe(true);
```
