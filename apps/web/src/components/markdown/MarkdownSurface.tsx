import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface MarkdownSurfaceProps {
    md: string | null | undefined;
}

export function MarkdownSurface({ md }: MarkdownSurfaceProps) {
    return (
        <div
            data-testid="markdown-surface"
            className="
        prose prose-sm max-w-none
        prose-invert
        text-slate-200
        prose-headings:text-slate-100
        prose-p:text-slate-300
        prose-li:text-slate-300
        prose-strong:text-slate-100
        prose-a:text-sky-300
        prose-code:text-amber-200
        prose-pre:bg-black/50
        prose-pre:border prose-pre:border-slate-800
      "
        >
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {md ?? ""}
            </ReactMarkdown>
        </div>
    );
}
