import { defineConfig } from '@playwright/test';

export default defineConfig({
    testDir: './tests/e2e',
    // Prevent discovery from nested git worktrees or node_modules that
    // may appear inside the repo tree during local development.
    testIgnore: ['**/.claude/**', '**/node_modules/**', '**/worktrees/**'],
    timeout: 120_000,
    workers: 4,
    reporter: 'list',
    use: {
        headless: true,
        baseURL: process.env.BASE_URL || 'http://localhost:5173',
    },
});
