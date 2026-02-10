import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypePrism from 'rehype-prism-plus';
import { Copy, Check, Info, AlertTriangle, AlertOctagon, Lightbulb, FileText } from 'lucide-react';
import { useOpenCodex } from '../../hooks/useOpenCodex';

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
        text-slate-300

        /* Headings */
        prose-h2:mt-8 prose-h2:mb-4 prose-h2:text-xl prose-h2:font-bold prose-h2:tracking-tight
        prose-h2:border-l-4 prose-h2:border-cyan-500/80 prose-h2:pl-4
        prose-h2:text-cyan-50
        
        prose-h3:mt-6 prose-h3:mb-3 prose-h3:text-lg prose-h3:font-semibold
        prose-h3:text-cyan-100/90

        /* Body & Lists */
        prose-p:leading-7 prose-p:my-4
        prose-li:my-2
        prose-ul:my-6 prose-ol:my-6
        
        /* Highlights */
        prose-strong:text-emerald-400 prose-strong:font-bold prose-strong:bg-emerald-950/30 prose-strong:px-1 prose-strong:rounded-sm

        /* Code & Links */
        prose-a:text-sky-400 hover:prose-a:text-sky-300 prose-a:underline hover:prose-a:no-underline prose-a:underline-offset-4
        prose-code:text-amber-200 prose-code:bg-amber-950/40 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:font-mono prose-code:text-[0.9em]
        prose-code:before:content-none prose-code:after:content-none
        prose-pre:bg-[#0d1117] prose-pre:border prose-pre:border-slate-800 prose-pre:shadow-xl prose-pre:rounded-lg

        /* Dividers */
        prose-hr:my-8 prose-hr:border-white/10
      "
        >
            <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypePrism]}
                components={{
                    pre: PreBlock,
                    blockquote: BlockquoteBlock,
                    a: ({ href, children, ...props }: any) => {
                        const openCodex = useOpenCodex();

                        if (href?.startsWith('codex:')) {
                            return (
                                <button
                                    onClick={() => openCodex(href)}
                                    className="text-sky-400 hover:text-sky-300 underline underline-offset-4 cursor-pointer inline-block"
                                    title={`Open Codex: ${href}`}
                                >
                                    {children}
                                </button>
                            );
                        }

                        return <a href={href} {...props}>{children}</a>;
                    }
                }}
            >
                {md ?? ""}
            </ReactMarkdown>
        </div>
    );
}


const PreBlock = ({ children, ...props }: any) => {
    const [copied, setCopied] = useState(false);

    // Extract text content safely
    const getTextContent = (node: React.ReactNode): string => {
        if (typeof node === 'string') return node;
        if (Array.isArray(node)) return node.map(getTextContent).join('');
        if (React.isValidElement(node) && node.props.children) {
            return getTextContent(node.props.children);
        }
        return '';
    };

    const handleCopy = () => {
        const text = getTextContent(children);
        if (text) {
            navigator.clipboard.writeText(text);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        }
    };

    return (
        <div className="relative group my-4">
            <div className="absolute right-2 top-2 z-10 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                    onClick={handleCopy}
                    className="p-1.5 bg-slate-700/80 hover:bg-slate-600 text-slate-300 rounded-md backdrop-blur-sm border border-slate-600"
                    title="Copy code"
                >
                    {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                </button>
            </div>
            <pre {...props} className="relative overflow-x-auto bg-[#0d1117] border border-slate-800 rounded-lg p-4">
                {children}
            </pre>
        </div>
    );
};

const BlockquoteBlock = ({ children, ...props }: any) => {
    // Detect Alert Syntax: > [!TIP] Content...
    // ReactMarkdown parses this as: Blockquote -> P -> text starting with [!TIP]

    const childrenArray = React.Children.toArray(children);
    const firstChild = childrenArray[0];

    let alertType: 'NOTE' | 'TIP' | 'IMPORTANT' | 'WARNING' | 'CAUTION' | null = null;
    let content = childrenArray;

    if (React.isValidElement(firstChild) && firstChild.type === 'p') {
        const pChildren = React.Children.toArray(firstChild.props.children);
        const firstText = pChildren[0];

        if (typeof firstText === 'string') {
            const match = firstText.match(/^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]/);
            if (match) {
                alertType = match[1] as any;
                // Remove the marker from the text
                const remainingText = firstText.substring(match[0].length).trim();

                // Reconstruct the paragraph without the marker
                const newPChildren = [
                    remainingText ? remainingText : null,
                    ...pChildren.slice(1)
                ].filter(Boolean);

                const newFirstP = React.cloneElement(firstChild as React.ReactElement, {}, ...newPChildren);
                content = [newFirstP, ...childrenArray.slice(1)];
            }
        }
    }

    if (alertType) {
        const styles = {
            NOTE: { icon: Info, color: 'text-blue-400', border: 'border-blue-500/50', bg: 'bg-blue-500/10' },
            TIP: { icon: Lightbulb, color: 'text-emerald-400', border: 'border-emerald-500/50', bg: 'bg-emerald-500/10' },
            IMPORTANT: { icon: FileText, color: 'text-violet-400', border: 'border-violet-500/50', bg: 'bg-violet-500/10' },
            WARNING: { icon: AlertTriangle, color: 'text-amber-400', border: 'border-amber-500/50', bg: 'bg-amber-500/10' },
            CAUTION: { icon: AlertOctagon, color: 'text-red-400', border: 'border-red-500/50', bg: 'bg-red-500/10' },
        };

        const style = styles[alertType];
        const Icon = style.icon;

        return (
            <div className={`my-4 rounded-lg border-l-4 p-4 ${style.border} ${style.bg}`}>
                <div className="flex items-start gap-3">
                    <Icon className={`w-5 h-5 shrink-0 mt-0.5 ${style.color}`} />
                    <div className="min-w-0 flex-1 space-y-2 text-slate-200">
                        {content}
                    </div>
                </div>
            </div>
        );
    }

    // Default Blockquote
    return (
        <blockquote {...props} className="border-l-4 border-slate-700 pl-4 italic text-slate-400 my-4">
            {children}
        </blockquote>
    );
};
