import React, { useMemo } from 'react';
import { MarkdownSurface } from '../../components/markdown/MarkdownSurface';
import { cn } from '../../lib/utils';
import { Tag, Globe, Layers } from 'lucide-react';
import { parseCodexContent } from './codexUtils';

interface CodexMarkdownProps {
    markdown: string;
    className?: string;
    // Optional overrides if metadata is passed externally
    overrideTitle?: string;
    overrideWorld?: string;
}

export const CodexMarkdown: React.FC<CodexMarkdownProps> = ({
    markdown,
    className,
    overrideTitle,
    overrideWorld
}) => {

    // Parse Metadata & Body
    const { content, metadata } = useMemo(() => {
        return parseCodexContent(markdown);
    }, [markdown]);

    // Derived Display Data
    const title = overrideTitle || metadata.title || 'Untitled Entry';
    const world = overrideWorld || metadata.world;
    const level = metadata.level;
    const tags = Array.isArray(metadata.tags) ? metadata.tags : (metadata.tags ? [metadata.tags] : []);

    return (
        <div className={cn("flex flex-col gap-6", className)}>

            {/* HERDER: Cyberdeck Style */}
            <div className="border-b border-white/10 pb-6 space-y-4">
                {/* Meta Row */}
                <div className="flex flex-wrap gap-3 items-center text-xs font-mono uppercase tracking-wider text-zinc-500">
                    {world && (
                        <div className="flex items-center gap-1.5 text-cyan-400 bg-cyan-950/30 px-2 py-0.5 rounded border border-cyan-800/50">
                            <Globe className="w-3 h-3" />
                            <span>{world}</span>
                        </div>
                    )}

                    {level && (
                        <div className="flex items-center gap-1.5 text-purple-400 bg-purple-950/30 px-2 py-0.5 rounded border border-purple-800/50">
                            <Layers className="w-3 h-3" />
                            <span>{level}</span>
                        </div>
                    )}

                    {tags.length > 0 && tags.map((t: string) => (
                        <div key={t} className="flex items-center gap-1.5 text-zinc-400 bg-zinc-900 px-2 py-0.5 rounded border border-zinc-800">
                            <Tag className="w-3 h-3" />
                            <span>{t}</span>
                        </div>
                    ))}
                </div>

                {/* Title */}
                <h1 className="text-3xl md:text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white via-zinc-200 to-zinc-500 tracking-tight">
                    {title}
                </h1>
            </div>

            {/* CONTENT: Markdown Surface */}
            <div className="min-h-[200px]">
                <MarkdownSurface md={content} />
            </div>
        </div>
    );
};
