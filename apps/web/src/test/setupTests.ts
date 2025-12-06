// Test setup file for Vitest + Testing Library
import '@testing-library/jest-dom/vitest';
import { afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';

// 🔒 Force-disable all unlock/god mode flags for tests
// This MUST run before any test imports useSkills or other hooks that read env
const originalEnv = import.meta.env;

Object.defineProperty(import.meta, 'env', {
    value: {
        ...originalEnv,
        VITE_DEV_UNLOCK_ALL: '0',
        VITE_UNLOCK_ALL: '0',
        VITE_LAYOUT_UNLOCK_ALL: '0',
    },
    writable: false,
    configurable: true,
});

afterEach(() => {
    cleanup();
});
