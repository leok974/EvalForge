import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

// Load scope config to respect enforcement rules
const scopePath = path.resolve(__dirname, '../../configs/curriculum_guardrail_scope.json');
const scope = JSON.parse(fs.readFileSync(scopePath, 'utf-8'));

const isActive = (worldId: string) => {
  return scope.active_worlds.includes(worldId);
};

const BASE_URL = 'http://127.0.0.1:5173';

test.describe('Workshop Smoke Tests', () => {
    
  test('workshop cards show descriptions and titles', async ({ page }) => {
    await page.goto(`${BASE_URL}/arcade/workshop`);
    
    // Check for quest cards
    const cards = page.locator('div[class*="QuestCard"]');
    await expect(cards.first()).toBeVisible();
    
    // Check descriptions are not empty
    const descriptions = cards.locator('p[class*="Description"]');
    const firstDesc = await descriptions.first().innerText();
    expect(firstDesc.length).toBeGreaterThan(0);
  });

  // Test a Python Systems quest (Active)
  test('active python quest has tutorial and run button', async ({ page }) => {
    const slug = 'python-systems-service-boundaries'; // A known active quest
    await page.goto(`${BASE_URL}/arcade/workshop/quests/${slug}`);
    
    // Verify Tutorial tab is visible and active by default or clickable
    const tutorialTab = page.locator('button:has-text("Tutorial")');
    await expect(tutorialTab).toBeVisible();
    
    // Verify "Run this file" button exists
    const runBtn = page.locator('button:has-text("Run this file")');
    await expect(runBtn).toBeVisible();
    
    // Verify code block in tutorial
    const codeBlock = page.locator('.prose pre');
    await expect(codeBlock.first()).toBeVisible();
  });

  test('example execution produces console output', async ({ page }) => {
    const slug = 'python-systems-service-boundaries';
    await page.goto(`${BASE_URL}/arcade/workshop/quests/${slug}`);
    
    // Click Run
    const runBtn = page.locator('button:has-text("Run this file")');
    await runBtn.click();
    
    // Check Console Output
    const consoleOutput = page.locator('div[class*="Console"]');
    // Wait for some output to appear (e.g., "Result:" or "--- Execution ---")
    await expect(consoleOutput).toContainText(/Execution|Result|---/i, { timeout: 10000 });
  });

  // Selenium Preview for active selenium quests (if any are active)
  test('selenium quest shows preview tab', async ({ page }) => {
    // Assuming python-selenium-basic-selectors is active or similar
    const slug = 'python-selenium-basic-selectors'; 
    await page.goto(`${BASE_URL}/arcade/workshop/quests/${slug}`);
    
    const previewTab = page.locator('button:has-text("Preview")');
    // We only fail if this is in ACTIVE scope. If not, we skip or warn (handled by playwright reporting)
    try {
        await expect(previewTab).toBeVisible({ timeout: 5000 });
    } catch (e) {
        if (isActive('world-python')) {
            throw e; // Fail CI if active
        } else {
            console.warn(`WARN: Preview tab missing for non-active quest ${slug}`);
        }
    }
  });

});
