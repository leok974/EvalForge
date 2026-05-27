# Tutorial: page.goto and Title Assertions

## Navigation

`page.goto(url)` is your entry point. It navigates the headless browser to the given URL and waits for the load event:

```typescript
await page.goto('/');          // Uses baseURL from config
await page.goto('https://example.com'); // Absolute URL
```

## Page-level Assertions

`expect(page).toHaveTitle()` checks the page's `<title>` element. It accepts a string (exact match) or a regex (partial match):

```typescript
await expect(page).toHaveTitle('CMS Login');         // exact
await expect(page).toHaveTitle(/CMS Login/i);        // regex, case-insensitive
```

## URL Assertion

You can also assert the URL after navigation:

```typescript
await expect(page).toHaveURL('/login');
await expect(page).toHaveURL(/login/);
```

## See in practice: pw-open-and-assert
