// @vitest-environment jsdom
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { CodexMarkdown } from '../CodexMarkdown';
import React from 'react';
import { MarkdownSurface } from '../../../components/markdown/MarkdownSurface';

// Mock dependencies
vi.mock('../../../components/markdown/MarkdownSurface', () => ({
    MarkdownSurface: ({ md }: any) => <div data-testid="markdown-surface">{md}</div>
}));

vi.mock('../../lib/utils', () => ({
    cn: (...inputs: any[]) => inputs.join(' ')
}));

// Mock Lucide icons
vi.mock('lucide-react', () => ({
    Tag: () => <div data-testid="icon-tag" />,
    Globe: () => <div data-testid="icon-globe" />,
    Layers: () => <div data-testid="icon-layers" />
}));

describe('CodexMarkdown', () => {
    it('renders basic markdown content', () => {
        render(<CodexMarkdown markdown="# Hello World" />);
        expect(screen.getByTestId('markdown-surface')).toHaveTextContent('# Hello World');
        expect(screen.getByText('Untitled Entry')).toBeInTheDocument();
    });

    it('parses YAML frontmatter correctly', () => {
        const markdown = `---
title: My Great Post
world: python
level: advanced
tags: [coding, snake]
---
# Actual Content
This is the body.`;

        render(<CodexMarkdown markdown={markdown} />);

        // Header Check
        expect(screen.getByText('My Great Post')).toBeInTheDocument(); // Title
        expect(screen.getByText('python')).toBeInTheDocument(); // World
        expect(screen.getByText('advanced')).toBeInTheDocument(); // Level
        expect(screen.getByText('coding')).toBeInTheDocument(); // Tag 1
        expect(screen.getByText('snake')).toBeInTheDocument(); // Tag 2

        // Body Check (Should not have frontmatter)
        expect(screen.getByTestId('markdown-surface')).toHaveTextContent('# Actual Content');
        expect(screen.getByTestId('markdown-surface')).not.toHaveTextContent('title: My Great Post');
    });

    it('parses legacy key-value lines correctly', () => {
        const markdown = `title: Legacy Title
world: javascript
id: some-id
# Real Content
Here we go.`;

        render(<CodexMarkdown markdown={markdown} />);

        expect(screen.getByText('Legacy Title')).toBeInTheDocument();
        expect(screen.getByText('javascript')).toBeInTheDocument();

        // Body Check
        expect(screen.getByTestId('markdown-surface')).toHaveTextContent('# Real Content');
        expect(screen.getByTestId('markdown-surface')).not.toHaveTextContent('title: Legacy Title');
    });

    it('uses overrides when provided', () => {
        const markdown = `---
title: Original Title
---
Body`;

        render(<CodexMarkdown markdown={markdown} overrideTitle="New Title" />);

        expect(screen.getByText('New Title')).toBeInTheDocument();
        expect(screen.queryByText('Original Title')).not.toBeInTheDocument();
    });

    it('handles mixed content gracefully', () => {
        const markdown = `Just some raw text without meta.`;
        render(<CodexMarkdown markdown={markdown} />);

        expect(screen.getByText('Untitled Entry')).toBeInTheDocument();
        expect(screen.getByTestId('markdown-surface')).toHaveTextContent('Just some raw text without meta.');
    });
});
