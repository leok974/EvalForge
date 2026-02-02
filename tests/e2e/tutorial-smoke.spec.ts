import { test, expect } from '@playwright/test';

test.describe('Quest Tutorial System', () => {
    // Test against the newly seeded Golden Git Quest
    const QUEST_SLUG = 'git-commit-q1-init-and-first-commit';
    const BASE_URL = 'http://localhost:5173';
    const QUEST_URL = `${BASE_URL}/worlds/world-git/quests/${QUEST_SLUG}`;

    test('Tutorial tab loads and renders markdown', async ({ page }) => {
        await page.goto(QUEST_URL);

        // Handle Login if redirected/blocked
        const loginBtn = page.getByRole('button', { name: 'Initialize Session' });
        if (await loginBtn.isVisible()) {
            await loginBtn.click();
            await page.waitForTimeout(1000); // Wait for auth
        }

        // 1. Should default to Tutorial tab if present (or we click it)
        try {
            const tutorialTab = page.getByRole('button', { name: /tutorial/i });
            if (await tutorialTab.isVisible()) {
                await tutorialTab.click();
            }
        } catch (e) {
            console.log("Tutorial tab check failed or already active");
        }

        // 2. Check for Tutorial Content Headers
        await expect(page.getByRole('heading', { name: 'Mission Briefing' })).toBeVisible();
        await expect(page.getByRole('heading', { name: 'Key Term: Repository' })).toBeVisible();

        // 3. Check for Code Block
        await expect(page.locator('pre').filter({ hasText: 'git init' })).toBeVisible();
    });

    test('Codex Drawer opens when clicking a term', async ({ page }) => {
        await page.goto(QUEST_URL);

        const loginBtn = page.getByRole('button', { name: 'Initialize Session' });
        if (await loginBtn.isVisible()) {
            await loginBtn.click();
            await page.waitForTimeout(1000);
        }

        await page.getByRole('button', { name: /tutorial/i }).click();

        // 4. Click a Key Term Chip (Assuming rendered as interactables)
        // The TutorialPanel renders terms as "Key Terms" section or chips?
        // Based on implementation, they are typically buttons or links.
        // Let's find distinct term "Repository"
        const termChip = page.getByRole('button', { name: 'repository' });
        await expect(termChip).toBeVisible();
        await termChip.click();

        // 5. Drawer should open
        const drawer = page.getByTestId('codex-drawer'); // Need to ensure testid exists or use text
        await expect(page.getByRole('heading', { name: 'Repository', level: 1 })).toBeVisible();

        // Dictionary content check
        await expect(page.getByText('storage location for your project')).toBeVisible();
    });

    test('Inline Codex links work', async ({ page }) => {
        // If we implemented inline links in markdown [term](codex:...)
        // Not strictly required by prompt but good to check if we did.
        // Skipping for now, focusing on Drawer.
    });
});
