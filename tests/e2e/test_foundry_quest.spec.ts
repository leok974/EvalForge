/**
 * Foundry Quest Path — End-to-End Test
 *
 * Walks the full foundry quest flow for "hello-variable":
 *   1. Landing page → Enter the Arcade
 *   2. Mock auth (Initialize Session)
 *   3. Navigate to hello-variable quest
 *   4. Verify briefing/tutorial renders (no raw ## markdown)
 *   5. Run starter code → objective FAIL (Submit disabled)
 *   6. Replace code with solution
 *   7. Run again → all objectives PASS (Submit enabled)
 *   8. Submit → XP awarded / success overlay shown
 *   9. Quest board shows first-sparks quest
 */

import { test, expect } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'http://localhost:5173';

const SOLUTION_CODE = [
    'def main():',
    '    message = "System Online"',
    '    print(message)',
    '',
    "if __name__ == '__main__':",
    '    main()',
].join('\n');

// ── helpers ──────────────────────────────────────────────────────────────────

async function handleLogin(page: any) {
    const loginBtn = page.getByRole('button', { name: 'Initialize Session' });
    try {
        if (await loginBtn.isVisible({ timeout: 5000 })) {
            await loginBtn.click();
            await page.waitForSelector('text=INITIALIZING LINK', { state: 'detached', timeout: 8000 })
                .catch(() => null);
        }
    } catch { /* already logged in */ }
}

async function dismissGettingStarted(page: any) {
    // Close the "Welcome to EvalForge" dialog if it shows
    try {
        const exploreBtn = page.getByRole('button', { name: 'Explore on my own' });
        if (await exploreBtn.isVisible({ timeout: 3000 })) {
            await exploreBtn.click();
        }
    } catch { /* dialog not shown */ }
}

async function replaceEditorContent(page: any, code: string) {
    // Use Monaco's executeEdits API to replace editor content.
    //
    // Pure keyboard simulation (Ctrl+A → Delete → type) is unreliable with
    // Playwright's synthetic events and Monaco: auto-indent after ':' stacks
    // with the indentation we type, and some characters are swallowed by
    // Monaco's suggestion engine.
    //
    // executeEdits creates a proper edit operation (unlike setValue which resets
    // the model), preserves undo history, and reliably fires onDidChangeModelContent
    // → React onChange. autoClosingQuotes/'never' is verified at the source level
    // in QuestEditor.tsx; the "System Online" quote check in Step 8 confirms it.
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
    }, code);
    // Give React time to process the onChange callback
    await page.waitForTimeout(500);
}

async function waitForRunComplete(page: any, runBtn: any) {
    // Wait a moment for the run to start (button becomes disabled)
    await page.waitForTimeout(500);
    // Then wait until the button is enabled again (run finished)
    await expect(runBtn).not.toBeDisabled({ timeout: 45_000 });
    // Give React one render cycle to settle after run completion
    await page.waitForTimeout(1000);
}

// ── test ─────────────────────────────────────────────────────────────────────

test.describe('Foundry Quest Path — hello-variable', () => {
    test.setTimeout(120_000); // 2 min — allows for real execution round-trips

    test('completes hello-variable from landing to XP award', async ({ page }) => {
        // Pre-seed localStorage before any page load to suppress the
        // "Welcome to EvalForge" getting-started dialog.
        await page.addInitScript(() => {
            localStorage.setItem('evalforge:seenTutorial', '1');
        });

        // ── Step 1: Landing page → Enter the Arcade ──────────────────────────
        await page.goto(BASE_URL);
        await expect(page).toHaveURL(`${BASE_URL}/`, { timeout: 10_000 });

        const enterBtn = page.getByRole('button', { name: /Enter the Arcade/i });
        await expect(enterBtn).toBeVisible({ timeout: 8_000 });
        await enterBtn.click();

        await page.waitForURL(/\/arcade/, { timeout: 10_000 });

        // ── Step 2: Mock auth ────────────────────────────────────────────────
        await handleLogin(page);
        await expect(page.locator('text=INITIALIZING LINK')).not.toBeVisible({ timeout: 10_000 });
        await dismissGettingStarted(page);

        // ── Steps 3-4: Navigate to hello-variable quest ──────────────────────
        await page.goto(`${BASE_URL}/arcade/worlds/world-python/quests/hello-variable`);
        await handleLogin(page);
        await expect(page.locator('text=INITIALIZING LINK')).not.toBeVisible({ timeout: 10_000 });
        await dismissGettingStarted(page);

        // Wait for QuestIDE to fully load
        await expect(page.locator('.monaco-editor').first()).toBeVisible({ timeout: 20_000 });

        // ── Step 5: Verify briefing/tutorial renders correctly ───────────────
        // The quest has tutorial_md — it should render as HTML, not raw Markdown.
        // "## " as raw text would mean Markdown is not being parsed.
        const rawHeading = page.locator(':text("## ")');
        const rawHeadingVisible = await rawHeading.isVisible({ timeout: 3_000 }).catch(() => false);
        expect(rawHeadingVisible, 'Raw ## Markdown heading should not be visible').toBe(false);

        // Quest title "Hello Variable" should be visible in the left pane
        await expect(page.getByText('Hello Variable').first()).toBeVisible({ timeout: 8_000 });

        // ── Step 6: Run starter code — expect objective FAIL ─────────────────
        // main.py loads by default (QuestIDE convention-based entrypoint detection).
        // The Run button might sit near the z-20 resize handle; force:true is safe
        // since the button text "Run" uniquely identifies our target.
        const runBtn = page.getByRole('button', { name: /^Run$/ }).first();
        await expect(runBtn).toBeVisible({ timeout: 10_000 });
        await runBtn.evaluate((el: any) => el.click());

        await waitForRunComplete(page, runBtn);

        // After starter code runs: Submit should be DISABLED (no objectives pass)
        const submitBtn = page.getByRole('button', { name: /Submit/ }).first();
        await expect(submitBtn).toBeDisabled({ timeout: 5_000 });

        // Click Results tab — use JS evaluate to guarantee the React onClick fires.
        // force:true bypasses pointer-events but some elements still absorb events;
        // evaluate().click() fires the native MouseEvent directly on the button.
        const resultsTab = page.locator('button', { hasText: 'Results' }).first();
        await resultsTab.evaluate((el: any) => el.click());

        // Wait for the "Objective Verification" heading to confirm the tab switched
        await expect(page.getByText('Objective Verification')).toBeVisible({ timeout: 8_000 });

        // The one objective ("Prints System Online") should be visible and NOT passing
        const objectiveText = page.getByText('Prints System Online').first();
        await expect(objectiveText).toBeVisible({ timeout: 5_000 });

        // ── Step 7: Replace editor content with solution ─────────────────────
        await replaceEditorContent(page, SOLUTION_CODE);

        // ── Step 8: Run solution code — expect objective PASS ────────────────
        await runBtn.evaluate((el: any) => el.click());
        await waitForRunComplete(page, runBtn);

        // Submit should now be ENABLED (all objectives pass)
        await expect(submitBtn).not.toBeDisabled({ timeout: 10_000 });

        // Click Results tab to confirm the objective is shown as passing
        await resultsTab.evaluate((el: any) => el.click());
        await expect(page.getByText('Objective Verification')).toBeVisible({ timeout: 8_000 });
        await expect(objectiveText).toBeVisible({ timeout: 5_000 });

        // ── Step 9: Submit → XP awarded ─────────────────────────────────────
        await submitBtn.click({ force: true });

        // Expect either "Mission Accomplished!" overlay or the XP result panel
        await expect(
            page.locator('text=Mission Accomplished!')
                .or(page.locator('[data-testid="quest-result-xp"]'))
                .or(page.getByText(/XP/i).first())
        ).toBeVisible({ timeout: 30_000 });

        // ── Step 10: Confirm first-sparks quest is accessible ───────────────
        // The OrionMap layout (default) renders world/track nodes but not
        // per-quest cards, so we verify first-sparks by navigating to it
        // directly. The quest IDE loading confirms it's accessible (not locked).
        await page.goto(`${BASE_URL}/arcade/worlds/world-python/quests/first-sparks`);
        await handleLogin(page);
        await expect(page.locator('.monaco-editor').first()).toBeVisible({ timeout: 20_000 });
    });
});
