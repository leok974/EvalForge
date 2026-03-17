import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

// Load scope config to respect enforcement rules
const scopePath = path.resolve(__dirname, '../../configs/curriculum_guardrail_scope.json');
const scope = JSON.parse(fs.readFileSync(scopePath, 'utf-8'));

const isActive = (worldId: string) => {
  return scope.active_worlds.includes(worldId);
};

const BASE_URL = 'http://localhost:5173';

test.describe('Workshop Smoke Tests', () => {
    
  test('workshop cards show descriptions and titles', async ({ page }) => {
    await page.goto(`${BASE_URL}/arcade/workshop`);
    
    // Check for quest cards
    const cards = page.locator('div[class*="QuestCard"]').first();
    await expect(cards).toBeVisible();
    
    // Check descriptions are not empty
    const descriptions = cards.locator('p[class*="Description"]');
    const firstDesc = await descriptions.first().innerText();
    expect(firstDesc.length).toBeGreaterThan(0);
  });

  // Test a Python Systems quest (Active)
  test('active python quest has tutorial and run button', async ({ page }) => {
    const slug = 'python-systems-service-boundaries'; // A known active quest
    await page.goto(`${BASE_URL}/arcade/workshop/quests/${slug}`);
    
    // Verify Tutorial tab is visible and active by default
    const tutorialTab = page.locator('button:has-text("Tutorial")');
    await expect(tutorialTab).toBeVisible();
    
    // Verify rendered tutorial content is non-empty and has meaningful text
    const tutorialProse = page.locator('.prose').first();
    await expect(tutorialProse).toBeVisible();
    const text = await tutorialProse.innerText();
    expect(text.length).toBeGreaterThan(100); // Expect meaningful explanation
    
    // Verify code block in tutorial
    const codeBlock = page.locator('.prose pre').first();
    await expect(codeBlock).toBeVisible();

    // Verify "Run this file" button exists
    const runBtn = page.locator('button:has-text("Run this file")');
    await expect(runBtn).toBeVisible();
  });

  test('example execution produces console output', async ({ page }) => {
    const slug = 'python-systems-service-boundaries';
    await page.goto(`${BASE_URL}/arcade/workshop/quests/${slug}`);
    
    // Verify we are looking at example.py or it's runnable
    const fileHeader = page.locator('div[class*="FileHeader"], div[class*="Tab"]');
    await expect(fileHeader.first()).toContainText(/example.py|Reference/i);

    // Click Run
    const runBtn = page.locator('button:has-text("Run this file")');
    await runBtn.click();
    
    // Check Console Output
    const consoleOutput = page.locator('div[class*="Console"]');
    
    // 1. Check for generic successful execution header
    await expect(consoleOutput).toContainText(/--- Running example.py ---/i, { timeout: 15000 });
    
    // 2. Check for concept-specific text (TicketRepository is core to this quest)
    await expect(consoleOutput).toContainText(/TicketRepository|InMemoryTicketRepo/i);
    
    // 3. Check for successful finality
    await expect(consoleOutput).toContainText(/Done|Success|Result:/i);
  });

  // Selenium Preview for active selenium quests
  test('selenium quest shows preview tab', async ({ page }) => {
    const slug = 'python-selenium-basic-selectors'; 
    await page.goto(`${BASE_URL}/arcade/workshop/quests/${slug}`);
    
    const previewTab = page.locator('button:has-text("Preview")');
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
