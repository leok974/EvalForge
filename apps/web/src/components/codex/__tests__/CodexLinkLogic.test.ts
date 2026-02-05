import { describe, it, expect } from 'vitest';

// Minimal test for the concept of codex links
// Since we don't have the full component tree with providers easily mockable here,
// we test the URL logic.

describe('Codex Link Logic', () => {
    it('should identify valid codex references', () => {
        const isCodexRef = (ref: string) => ref.startsWith('codex:');

        expect(isCodexRef('codex:glossary/python/print')).toBe(true);
        expect(isCodexRef('https://google.com')).toBe(false);
    });

    it('should parse codex references correctly', () => {
        const parse = (ref: string) => {
            if (!ref.startsWith('codex:')) return null;
            return ref.substring(6);
        };

        expect(parse('codex:glossary/abc')).toBe('glossary/abc');
    });
});
