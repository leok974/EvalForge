import React, { useState } from 'react';
import { Check, Copy, FileInput } from 'lucide-react';
import { cn } from '@/lib/utils';
// Note: PrismAsyncLight is often better for bundle size, checking what was used before.
// TutorialPanel.tsx used generic code block without highlighting lib.
// We'll stick to simple rendering for now to match style but add buttons.

interface CodeBlockProps {
    children: React.ReactNode;
    className?: string;
    inline?: boolean;
    onPaste?: () => void;
    canPaste?: boolean;
    pasteLabel?: string;
    [key: string]: any;
}

export function CodeBlock({
    inline,
    className,
    children,
    onPaste,
    canPaste,
    pasteLabel = "Paste",
    ...props
}: CodeBlockProps) {
    const [copied, setCopied] = useState(false);
    const [pasted, setPasted] = useState(false);

    // Extract text content from children
    const codeText = String(children).replace(/\n$/, '');

    const handleCopy = async () => {
        await navigator.clipboard.writeText(codeText);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    const handlePaste = () => {
        if (onPaste) {
            onPaste();
            setPasted(true);
            setTimeout(() => setPasted(false), 2000);
        }
    };

    if (inline) {
        return (
            <code className={cn("bg-gray-100 dark:bg-gray-800 rounded px-1.5 py-0.5 text-sm font-mono", className)} {...props}>
                {children}
            </code>
        );
    }

    return (
        <div className="relative group my-4 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-800">
            <div className="absolute right-2 top-2 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity z-10">
                {canPaste && onPaste && (
                    <button
                        onClick={handlePaste}
                        className="p-1.5 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-100 transition-colors flex items-center gap-1 text-xs font-medium px-2"
                        title="Paste into editor"
                    >
                        {pasted ? <Check className="w-3.5 h-3.5" /> : <FileInput className="w-3.5 h-3.5" />}
                        {pasted ? 'Pasted!' : pasteLabel}
                    </button>
                )}

                <button
                    onClick={handleCopy}
                    className="p-1.5 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-100 transition-colors"
                    title="Copy code"
                >
                    {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                </button>
            </div>

            <pre className={cn("bg-gray-50 dark:bg-gray-900 p-4 overflow-x-auto text-sm", className)} {...props}>
                <code className={className} {...props}>
                    {children}
                </code>
            </pre>
        </div>
    );
}
