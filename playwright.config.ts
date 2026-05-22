import { defineConfig } from '@playwright/test';

export default defineConfig({
    testDir: './tests/e2e',
    timeout: 120_000,
    workers: 4,
    reporter: 'list',
    use: {
        headless: true,
        baseURL: process.env.BASE_URL || 'http://localhost:5173',
    },
});
