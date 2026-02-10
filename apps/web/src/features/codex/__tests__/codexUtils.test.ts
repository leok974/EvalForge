
import { describe, it, expect } from 'vitest';
import { parseCodexContent } from '../codexUtils';

describe('codexUtils', () => {
    describe('parseCodexContent', () => {
        it('parses YAML frontmatter correctly', () => {
            const markdown = `---
title: My Great Post
world: python
level: advanced
tags: [coding, snake]
---
# Actual Content
This is the body.`;

            const { content, metadata } = parseCodexContent(markdown);

            expect(metadata.title).toBe('My Great Post');
            expect(metadata.world).toBe('python');
            expect(metadata.level).toBe('advanced');
            expect(metadata.tags).toEqual(['coding', 'snake']);
            expect(content).toBe('# Actual Content\nThis is the body.');
        });

        it('parses legacy key-value lines correctly', () => {
            const markdown = `title: Legacy Title
world: javascript
id: some-id
# Real Content
Here we go.`;

            const { content, metadata } = parseCodexContent(markdown);

            expect(metadata.title).toBe('Legacy Title');
            expect(metadata.world).toBe('javascript');
            expect(metadata.id).toBe('some-id');
            expect(content).toBe('# Real Content\nHere we go.');
        });

        it('handles mixed content gracefully', () => {
            const markdown = `Just some raw text without meta.`;
            const { content, metadata } = parseCodexContent(markdown);

            expect(metadata).toEqual({});
            expect(content).toBe('Just some raw text without meta.');
        });

        it('respects whitelist for legacy keys', () => {
            const markdown = `definition: A thing.
title: Real Title
world: python`;

            // "definition" is NOT in whitelist, so it should be treated as content.
            // However, our parser stops at the first non-header line.
            // If "definition: ..." is line 1, it might check it.
            // "definition" is NOT in whitelist, so `inHeader` becomes false immediately.

            const { content, metadata } = parseCodexContent(markdown);

            expect(metadata).toEqual({}); // No meta extracted because first line failed whitelist
            expect(content).toContain('definition: A thing.');
            expect(content).toContain('title: Real Title');
        });
    });
});
