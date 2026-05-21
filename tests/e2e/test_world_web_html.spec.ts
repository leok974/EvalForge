import { test, expect } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'http://localhost:5173';

const SOLUTION_CODE = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>EvalForge HTML</title>
</head>
<body>
  <main data-testid="app">Hello, Web</main>
</body>
</html>
`;

test.describe('world-web html — html-ignition', () => {
    test.setTimeout(120_000);

    test('HTML Ignition: Page Skeleton end-to-end', async ({ page }) => {
        await page.addInitScript(() => {
            localStorage.setItem('evalforge:seenTutorial', '1');
        });

        // 1. Navigate to quest IDE
        await page.goto(`${BASE_URL}/arcade/worlds/world-web/quests/html-ignition`);
        // handle login
        const loginBtn = page.getByRole('button', { name: 'Initialize Session' });
        if (await loginBtn.isVisible({ timeout: 5000 }).catch(() => false))
            await loginBtn.click();
        await page.waitForSelector('text=INITIALIZING LINK', { state: 'detached', timeout: 8000 }).catch(() => null);

        // 2. Wait for IDE to load
        await expect(page.locator('.monaco-editor').first()).toBeVisible({ timeout: 20_000 });

        // 3. Run starter code — expect FAIL
        const runBtn = page.getByRole('button', { name: /^Run$/ }).first();
        await expect(runBtn).toBeVisible({ timeout: 10_000 });
        await runBtn.evaluate((el: any) => el.click());
        await page.waitForTimeout(500);
        await expect(runBtn).not.toBeDisabled({ timeout: 45_000 });
        await page.waitForTimeout(1000);

        const submitBtn = page.getByRole('button', { name: /Submit/ }).first();
        await expect(submitBtn).toBeDisabled({ timeout: 5_000 });

        // 4. Replace with solution (index.html is the active entrypoint for html quest)
        await page.evaluate((newCode: string) => {
            const win = window as any;
            if (win.monaco?.editor) {
                const editors = win.monaco.editor.getEditors();
                if (editors.length > 0) {
                    const model = editors[0].getModel();
                    if (model) {
                        editors[0].executeEdits('e2e-replace', [{
                            range: model.getFullModelRange(),
                            text: newCode,
                        }]);
                    }
                }
            }
        }, SOLUTION_CODE);
        await page.waitForTimeout(500);

        // 5. Run solution — expect PASS
        await runBtn.evaluate((el: any) => el.click());
        await page.waitForTimeout(500);
        await expect(runBtn).not.toBeDisabled({ timeout: 45_000 });
        await page.waitForTimeout(1000);

        await expect(submitBtn).not.toBeDisabled({ timeout: 10_000 });

        // 6. Submit → XP
        await submitBtn.click({ force: true });
        await expect(
            page.locator('text=Mission Accomplished')
                .or(page.locator('[data-testid="quest-result-xp"]'))
                .or(page.locator('h2').filter({ hasText: /Mission Accomplished/i }))
                .or(page.getByText('XP Earned').first())
        ).toBeVisible({ timeout: 30_000 });
    });
});
